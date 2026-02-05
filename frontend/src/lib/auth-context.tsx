/**
 * User context and authentication utilities.
 * Extracts user information from JWT token.
 */
"use client";

import { createContext, useContext, useEffect, useState } from "react";

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  refreshUser: () => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  isLoading: true,
  refreshUser: () => {},
});

/**
 * Decode JWT token and extract user information
 */
function decodeToken(token: string): User | null {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    const payload = JSON.parse(jsonPayload);

    return {
      id: payload.sub,
      email: payload.email,
      name: payload.name,
    };
  } catch (error) {
    console.error('Failed to decode token:', error);
    return null;
  }
}

/**
 * Get current user from JWT token
 */
export function getCurrentUser(): User | null {
  if (typeof window === 'undefined') return null;

  const token = localStorage.getItem('auth_token');
  if (!token) return null;

  return decodeToken(token);
}

/**
 * Auth Provider Component
 */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const refreshUser = () => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      const userData = decodeToken(token);
      setUser(userData);
    } else {
      setUser(null);
    }
  };

  useEffect(() => {
    refreshUser();
    setIsLoading(false);
  }, []);

  return (
    <AuthContext.Provider value={{ user, isLoading, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

/**
 * Hook to access auth context
 */
export function useAuth() {
  return useContext(AuthContext);
}
