/**
 * Chat component for AI-powered task management.
 *
 * This component provides the main chat interface where users can
 * interact with the AI assistant to manage their tasks.
 */

'use client';

import { useState, useEffect, useRef } from 'react';
import { ChatMessage } from './ChatMessage';
import { Message } from '@/types/chat';
import { getConversation, sendChatMessage } from '@/lib/api';

interface ChatProps {
  conversationId?: string | null;
  onConversationChange?: (conversationId: string) => void;
}

export default function Chat({ conversationId: initialConversationId, onConversationChange }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(initialConversationId || null);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load conversation history when conversation ID changes
  useEffect(() => {
    if (initialConversationId && initialConversationId !== conversationId) {
      loadConversationHistory(initialConversationId);
    }
  }, [initialConversationId]);

  const loadConversationHistory = async (convId: string) => {
    try {
      setLoadingHistory(true);
      setError(null);

      const conversation = await getConversation(convId);

      // Convert to Message format
      const historyMessages: Message[] = conversation.messages.map(msg => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
        created_at: msg.created_at
      }));

      setMessages(historyMessages);
      setConversationId(convId);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load conversation history');
    } finally {
      setLoadingHistory(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      created_at: new Date().toISOString()
    };

    // Optimistic UI update
    setMessages(prev => [...prev, userMessage]);
    const messageText = input;
    setInput('');
    setLoading(true);
    setError(null);

    try {
      // Use the API function which handles authentication automatically
      const data = await sendChatMessage(messageText, conversationId);

      // Update conversation ID if this was a new conversation
      if (!conversationId) {
        setConversationId(data.conversation_id);
        if (onConversationChange) {
          onConversationChange(data.conversation_id);
        }
      }

      // Add assistant message
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.message,
        created_at: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      // Remove optimistic user message on error
      setMessages(prev => prev.slice(0, -1));
      setInput(messageText); // Restore input
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (loadingHistory) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-500">Loading conversation...</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Messages area */}
      <div
        className="flex-1 overflow-y-auto p-4 space-y-4"
        role="log"
        aria-live="polite"
        aria-label="Chat messages"
      >
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <p className="text-lg font-medium">Welcome to AI Task Assistant!</p>
            <p className="mt-2">Ask me to create, view, update, or complete your tasks.</p>
            <p className="mt-4 text-sm">Try: "Add a task to buy groceries tomorrow"</p>
          </div>
        )}

        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}

        {loading && (
          <div className="flex justify-start" role="status" aria-label="AI is typing">
            <div className="bg-gray-200 rounded-lg p-3 max-w-[70%]">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
              <span className="sr-only">AI is typing</span>
            </div>
          </div>
        )}

        {error && (
          <div
            className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded"
            role="alert"
            aria-live="assertive"
          >
            <p className="font-medium">Error</p>
            <p className="text-sm">{error}</p>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t p-4 bg-white">
        <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex gap-2">
          <label htmlFor="chat-input" className="sr-only">
            Type your message
          </label>
          <input
            id="chat-input"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={loading}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
            maxLength={2000}
            aria-label="Chat message input"
            aria-describedby="char-count"
          />
          <button
            type="submit"
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            aria-label={loading ? 'Sending message' : 'Send message'}
          >
            {loading ? 'Sending...' : 'Send'}
          </button>
        </form>
        <p id="char-count" className="text-xs text-gray-500 mt-2" aria-live="polite">
          {input.length}/2000 characters
        </p>
      </div>
    </div>
  );
}
