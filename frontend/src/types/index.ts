/**
 * TypeScript type definitions for the application.
 * Matches backend SQLModel schemas.
 */

export interface User {
  id: string;
  email: string;
  name?: string;
  emailVerified: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Task {
  id: number;
  userId: string;
  title: string;
  description?: string;
  category?: string;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  category?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  category?: string;
}

export interface TasksResponse {
  tasks: Task[];
  total: number;
  filters: {
    status: string | null;
    category: string | null;
    search: string | null;
  };
}

export interface AuthResponse {
  user: User;
  token: string;
  expiresAt: string;
}

export interface ErrorResponse {
  error: string;
  code?: string;
  details?: Array<{
    field: string;
    message: string;
  }>;
}
