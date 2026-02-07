/**
 * TypeScript types for AI chat functionality.
 *
 * These types define the structure of chat-related data
 * exchanged between frontend and backend.
 */

/**
 * Request payload for sending a chat message.
 */
export interface ChatRequest {
  message: string;
  conversation_id?: string | null;
}

/**
 * Response payload from chat endpoint.
 */
export interface ChatResponse {
  conversation_id: string;
  message: string;
  tool_calls?: ToolCallInfo[];
}

/**
 * Information about AI tool invocations (for transparency).
 */
export interface ToolCallInfo {
  tool_name: string;
  success: boolean;
}

/**
 * Individual message in a conversation.
 */
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

/**
 * Conversation metadata.
 */
export interface Conversation {
  id: string;
  title: string;
  status: 'active' | 'archived';
  created_at: string;
  updated_at: string;
}

/**
 * Conversation with full message history.
 */
export interface ConversationDetail extends Conversation {
  messages: Message[];
}

/**
 * Request to create a new conversation.
 */
export interface CreateConversationRequest {
  title?: string;
}

/**
 * Request to update conversation properties.
 */
export interface UpdateConversationRequest {
  title?: string;
  status?: 'active' | 'archived';
}

/**
 * List of conversations with pagination info.
 */
export interface ConversationListResponse {
  conversations: Conversation[];
  total: number;
}

/**
 * Error response from API.
 */
export interface ErrorResponse {
  error: string;
  details?: Record<string, any>;
}
