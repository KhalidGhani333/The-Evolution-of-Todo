/**
 * API client for making authenticated requests to the backend.
 * Handles JWT token management and request headers.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Get the JWT token from storage
 */
function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('auth_token');
}

/**
 * Set the JWT token in storage (both localStorage and cookies)
 */
export function setToken(token: string): void {
  if (typeof window === 'undefined') return;

  // Store in localStorage
  localStorage.setItem('auth_token', token);

  // Store in cookies for middleware
  document.cookie = `auth_token=${token}; path=/; max-age=${7 * 24 * 60 * 60}; SameSite=Lax`;
}

/**
 * Remove the JWT token from storage (both localStorage and cookies)
 */
export function removeToken(): void {
  if (typeof window === 'undefined') return;

  // Remove from localStorage
  localStorage.removeItem('auth_token');

  // Remove from cookies
  document.cookie = 'auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
}

/**
 * Sign out the current user
 */
export async function signOut(): Promise<void> {
  removeToken();
  if (typeof window !== 'undefined') {
    window.location.href = '/signin';
  }
}

/**
 * Make an authenticated API request
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  // Add Authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Handle 401 Unauthorized - token expired or invalid
  if (response.status === 401) {
    removeToken();
    if (typeof window !== 'undefined') {
      window.location.href = '/signin';
    }
    throw new Error('Unauthorized');
  }

  // Handle 403 Forbidden - insufficient permissions
  if (response.status === 403) {
    throw new Error('Forbidden: Cannot access this resource');
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Request failed' }));
    throw new Error(error.error || error.detail || 'Request failed');
  }

  return response.json();
}

/**
 * API client methods
 */
export const api = {
  get: <T>(endpoint: string) => apiRequest<T>(endpoint, { method: 'GET' }),

  post: <T>(endpoint: string, data: unknown) =>
    apiRequest<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  put: <T>(endpoint: string, data: unknown) =>
    apiRequest<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  patch: <T>(endpoint: string, data: unknown) =>
    apiRequest<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  delete: <T>(endpoint: string) =>
    apiRequest<T>(endpoint, { method: 'DELETE' }),
};
