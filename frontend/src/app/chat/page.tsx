/**
 * Chat page for AI-powered task management.
 *
 * This page provides the main interface for users to interact
 * with the AI assistant to manage their tasks, with conversation
 * management sidebar.
 */

'use client';

import { useState } from 'react';
import Chat from '@/components/Chat';
import { ConversationList } from '@/components/ConversationList';

export default function ChatPage() {
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [showSidebar, setShowSidebar] = useState(true);

  const handleSelectConversation = (conversationId: string) => {
    setCurrentConversationId(conversationId);
  };

  const handleNewConversation = () => {
    setCurrentConversationId(null);
  };

  const handleConversationChange = (conversationId: string) => {
    setCurrentConversationId(conversationId);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-2 sm:px-4 py-4 sm:py-8">
        {/* Header */}
        <div className="mb-4 sm:mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">AI Task Assistant</h1>
            <p className="text-gray-600 mt-1 sm:mt-2 text-sm sm:text-base">
              Manage your tasks using natural language. Just tell me what you need!
            </p>
          </div>
          <button
            onClick={() => setShowSidebar(!showSidebar)}
            className="lg:hidden px-3 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 text-sm"
            aria-label={showSidebar ? 'Hide conversations' : 'Show conversations'}
          >
            {showSidebar ? 'Hide' : 'Show'}
          </button>
        </div>

        {/* Main content with sidebar */}
        <div className="flex flex-col lg:flex-row gap-4 h-[calc(100vh-180px)] sm:h-[calc(100vh-250px)]">
          {/* Sidebar - Conversation list */}
          {showSidebar && (
            <div className="w-full lg:w-80 bg-white rounded-lg shadow-lg overflow-hidden h-64 lg:h-auto">
              <ConversationList
                currentConversationId={currentConversationId}
                onSelectConversation={handleSelectConversation}
                onNewConversation={handleNewConversation}
              />
            </div>
          )}

          {/* Main chat area */}
          <div className="flex-1 bg-white rounded-lg shadow-lg overflow-hidden min-h-[400px]">
            <Chat
              conversationId={currentConversationId}
              onConversationChange={handleConversationChange}
            />
          </div>
        </div>

        {/* Help text */}
        <div className="mt-4 text-xs sm:text-sm text-gray-500">
          <p className="font-medium mb-2">Try these commands:</p>
          <ul className="list-disc list-inside space-y-1">
            <li>"Add a task to buy groceries tomorrow"</li>
            <li>"What are my tasks?"</li>
            <li>"Mark the groceries task as done"</li>
            <li>"Delete the old reminder"</li>
            <li>"Update my report task deadline to Friday"</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
