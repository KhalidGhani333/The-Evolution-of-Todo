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

  // Handle 204 No Content (e.g., DELETE operations)
  if (response.status === 204) {
    return undefined as T;
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

/**
 * Chat API functions
 */
import {
  ChatRequest,
  ChatResponse,
  Conversation,
  ConversationDetail,
  ConversationListResponse,
  CreateConversationRequest,
  UpdateConversationRequest
} from '@/types/chat';

export async function sendChatMessage(
  message: string,
  conversationId?: string | null
): Promise<ChatResponse> {
  const request: ChatRequest = {
    message,
    conversation_id: conversationId
  };

  return api.post<ChatResponse>('/api/chat', request);
}

export async function listConversations(
  status: string = 'active',
  limit: number = 20,
  offset: number = 0
): Promise<ConversationListResponse> {
  return api.get<ConversationListResponse>(
    `/api/chat/conversations?status=${status}&limit=${limit}&offset=${offset}`
  );
}

export async function getConversation(
  conversationId: string,
  limit: number = 50
): Promise<ConversationDetail> {
  return api.get<ConversationDetail>(
    `/api/chat/conversations/${conversationId}?limit=${limit}`
  );
}

export async function createConversation(
  title?: string
): Promise<Conversation> {
  const request: CreateConversationRequest = { title };
  return api.post<Conversation>('/api/chat/conversations', request);
}

export async function updateConversation(
  conversationId: string,
  updates: UpdateConversationRequest
): Promise<Conversation> {
  return api.patch<Conversation>(
    `/api/chat/conversations/${conversationId}`,
    updates
  );
}

export async function deleteConversation(
  conversationId: string
): Promise<void> {
  return api.delete<void>(`/api/chat/conversations/${conversationId}`);
}

/**
 * Task API functions
 */
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  category?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TasksResponse {
  tasks: Task[];
  total: number;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
  category?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  category?: string;
  completed?: boolean;
}

export async function getTasks(): Promise<TasksResponse> {
  return api.get<TasksResponse>('/api/tasks');
}

export async function createTask(data: CreateTaskRequest): Promise<Task> {
  return api.post<Task>('/api/tasks', data);
}

export async function updateTask(taskId: number, data: UpdateTaskRequest): Promise<Task> {
  return api.patch<Task>(`/api/tasks/${taskId}`, data);
}

export async function deleteTask(taskId: number): Promise<void> {
  return api.delete<void>(`/api/tasks/${taskId}`);
}

export async function completeTask(taskId: number): Promise<Task> {
  return api.post<Task>(`/api/tasks/${taskId}/complete`, {});
}
