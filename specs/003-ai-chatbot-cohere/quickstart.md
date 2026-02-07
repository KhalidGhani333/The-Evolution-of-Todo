# Quickstart Guide: AI-Powered Todo Chatbot

**Feature**: Phase III - AI Chatbot Integration
**Created**: 2026-02-06
**Audience**: Developers implementing the chatbot feature

## Overview

This guide provides step-by-step instructions for implementing the AI-powered chatbot feature using Cohere API. Follow these steps in order to build a working conversational interface for task management.

---

## Prerequisites

- Phase II completed and functional (Next.js frontend, FastAPI backend, PostgreSQL database)
- Cohere API key (free tier available at https://cohere.com)
- Python 3.13+ with UV package manager
- Node.js 18+ for frontend
- PostgreSQL database (Neon or local)

---

## Step 1: Environment Setup

### 1.1 Install Cohere SDK

```bash
cd backend
pip install cohere>=5.0.0
```

### 1.2 Configure Environment Variables

Add to `backend/.env`:
```env
COHERE_API_KEY=your_cohere_api_key_here
CHAT_RATE_LIMIT=60  # Requests per minute per user
CHAT_HISTORY_LIMIT=50  # Max messages per conversation
```

### 1.3 Verify Existing Configuration

Ensure these are already set from Phase II:
```env
DATABASE_URL=postgresql://user:pass@host/db
JWT_SECRET=your_jwt_secret
```

---

## Step 2: Database Migration

### 2.1 Create Migration File

Create `backend/migrations/003_add_chat_tables.sql`:

```sql
-- Create conversations table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL DEFAULT 'New Conversation',
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'archived')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    tool_results JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_conversations_user_created ON conversations(user_id, created_at);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);
```

### 2.2 Run Migration

```bash
# Using psql
psql $DATABASE_URL -f backend/migrations/003_add_chat_tables.sql

# Or using SQLModel (if you have migration script)
python backend/scripts/run_migrations.py
```

### 2.3 Verify Migration

```bash
psql $DATABASE_URL -c "\dt conversations messages"
```

---

## Step 3: Backend Implementation

### 3.1 Create Data Models

Create `backend/src/models/conversation.py`:

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from enum import Enum
import uuid

class ConversationStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(default="New Conversation", max_length=200)
    status: ConversationStatus = Field(default=ConversationStatus.ACTIVE, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", nullable=False, index=True)
    role: MessageRole = Field(nullable=False, index=True)
    content: str = Field(nullable=False, max_length=10000)
    tool_calls: Optional[str] = Field(default=None)
    tool_results: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    conversation: Conversation = Relationship(back_populates="messages")
```

### 3.2 Create Chat Service

Create `backend/src/services/chat_service.py`:

```python
import cohere
import os
from typing import Dict, Any, List, Optional
from sqlmodel import Session, select
from src.models.conversation import Conversation, Message, MessageRole
from src.services.chat_tools import ChatTools
import logging

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
        self.tools = self._define_tools()

    def _define_tools(self) -> List[Dict]:
        """Define Cohere tool schemas."""
        return [
            {
                "name": "add_task",
                "description": "Create a new task for the user",
                "parameter_definitions": {
                    "title": {"description": "Task title", "type": "str", "required": True},
                    "description": {"description": "Task description", "type": "str", "required": False},
                    "category": {"description": "Task category", "type": "str", "required": False}
                }
            },
            {
                "name": "list_tasks",
                "description": "Retrieve all tasks with optional filters",
                "parameter_definitions": {
                    "status": {"description": "Filter by status", "type": "str", "required": False},
                    "category": {"description": "Filter by category", "type": "str", "required": False}
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameter_definitions": {
                    "task_id": {"description": "Task ID", "type": "int", "required": True}
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task permanently",
                "parameter_definitions": {
                    "task_id": {"description": "Task ID", "type": "int", "required": True}
                }
            },
            {
                "name": "update_task",
                "description": "Update task properties",
                "parameter_definitions": {
                    "task_id": {"description": "Task ID", "type": "int", "required": True},
                    "title": {"description": "New title", "type": "str", "required": False},
                    "description": {"description": "New description", "type": "str", "required": False},
                    "category": {"description": "New category", "type": "str", "required": False}
                }
            }
        ]

    def chat(
        self,
        session: Session,
        user_id: str,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process chat message and return AI response."""
        try:
            # Get or create conversation
            if conversation_id:
                conversation = self._get_conversation(session, user_id, conversation_id)
            else:
                conversation = self._create_conversation(session, user_id)

            # Get conversation history
            chat_history = self._get_chat_history(session, conversation.id)

            # Call Cohere API
            response = self.co.chat(
                model="command-r-plus",
                message=message,
                chat_history=chat_history,
                tools=self.tools,
                temperature=0.3
            )

            # Handle tool calls if any
            if response.tool_calls:
                tool_results = self._execute_tools(session, user_id, response.tool_calls)

                # Get final response with tool results
                final_response = self.co.chat(
                    model="command-r-plus",
                    message="",
                    chat_history=chat_history + [{"role": "USER", "message": message}],
                    tools=self.tools,
                    tool_results=tool_results
                )

                assistant_message = final_response.text
            else:
                assistant_message = response.text

            # Save messages to database
            self._save_message(session, conversation.id, MessageRole.USER, message)
            self._save_message(session, conversation.id, MessageRole.ASSISTANT, assistant_message)

            return {
                "conversation_id": conversation.id,
                "message": assistant_message
            }

        except Exception as e:
            logger.error(f"Chat error: {e}")
            raise

    def _execute_tools(
        self,
        session: Session,
        user_id: str,
        tool_calls: List
    ) -> List[Dict]:
        """Execute tool calls and return results."""
        results = []
        for tool_call in tool_calls:
            result = ChatTools.execute_tool(
                tool_name=tool_call.name,
                parameters=tool_call.parameters,
                user_id=user_id,
                session=session
            )
            results.append({
                "call": {"name": tool_call.name, "parameters": tool_call.parameters},
                "outputs": [result]
            })
        return results
```

### 3.3 Create Chat Tools

Create `backend/src/services/chat_tools.py`:

```python
from typing import Dict, Any, Optional
from sqlmodel import Session
from src.services.task_service import TaskService
from src.models.task import TaskCreate, TaskUpdate

class ChatTools:
    @staticmethod
    def execute_tool(
        tool_name: str,
        parameters: Dict[str, Any],
        user_id: str,
        session: Session
    ) -> Dict[str, Any]:
        """Route tool execution to appropriate handler."""
        tool_map = {
            "add_task": ChatTools.add_task,
            "list_tasks": ChatTools.list_tasks,
            "complete_task": ChatTools.complete_task,
            "delete_task": ChatTools.delete_task,
            "update_task": ChatTools.update_task
        }

        if tool_name not in tool_map:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}

        return tool_map[tool_name](session=session, user_id=user_id, **parameters)

    @staticmethod
    def add_task(session: Session, user_id: str, title: str, **kwargs) -> Dict:
        try:
            task_data = TaskCreate(title=title, **kwargs)
            task = TaskService.create_task(session, user_id, task_data)
            return {"success": True, "message": f"Task '{task.title}' created"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Implement other tool methods similarly...
```

### 3.4 Create API Endpoints

Create `backend/src/api/chat.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel, Field
from src.database import get_session
from src.auth import get_current_user
from src.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])
chat_service = ChatService()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None

@router.post("")
async def send_message(
    request: ChatRequest,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """Send a chat message and get AI response."""
    try:
        response = chat_service.chat(
            session=session,
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Step 4: Frontend Implementation

### 4.1 Create Chat Component

Create `frontend/src/components/Chat.tsx`:

```typescript
'use client';

import { useState } from 'react';
import { sendChatMessage } from '@/lib/api';

export default function Chat() {
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await sendChatMessage(input, conversationId);
      setConversationId(response.conversation_id);
      setMessages(prev => [...prev, { role: 'assistant', content: response.message }]);
    } catch (error) {
      console.error('Chat error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      <div className="flex-1 overflow-y-auto space-y-4 mb-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[70%] p-3 rounded-lg ${
              msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
        {loading && <div className="text-gray-500">AI is thinking...</div>}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message..."
          className="flex-1 p-2 border rounded"
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
```

### 4.2 Add API Function

Add to `frontend/src/lib/api.ts`:

```typescript
export async function sendChatMessage(message: string, conversationId?: string | null) {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ message, conversation_id: conversationId })
  });

  if (!response.ok) throw new Error('Chat request failed');
  return response.json();
}
```

### 4.3 Create Chat Page

Create `frontend/src/app/chat/page.tsx`:

```typescript
import Chat from '@/components/Chat';

export default function ChatPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">AI Task Assistant</h1>
      <Chat />
    </div>
  );
}
```

---

## Step 5: Testing

### 5.1 Test Backend

```bash
cd backend
pytest tests/test_chat_service.py -v
```

### 5.2 Test API Endpoints

```bash
# Start backend
uvicorn src.main:app --reload

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

### 5.3 Test Frontend

```bash
cd frontend
npm run dev
# Navigate to http://localhost:3000/chat
```

---

## Step 6: Deployment

### 6.1 Backend Deployment

1. Add COHERE_API_KEY to production environment variables
2. Run database migrations on production database
3. Deploy backend to Hugging Face Spaces or your hosting platform

### 6.2 Frontend Deployment

1. Update API_URL in frontend/.env.production
2. Build and deploy to Vercel: `vercel --prod`

---

## Troubleshooting

### Issue: Cohere API errors
- **Solution**: Check API key is valid, check rate limits, verify internet connection

### Issue: Database connection errors
- **Solution**: Verify DATABASE_URL, check database is running, verify migrations ran successfully

### Issue: JWT authentication fails
- **Solution**: Verify JWT_SECRET matches between frontend and backend, check token expiration

### Issue: Tool calls not working
- **Solution**: Check TaskService methods exist, verify user_id is passed correctly, check database permissions

---

## Next Steps

1. Implement conversation management endpoints (list, get, update, delete)
2. Add conversation history UI
3. Implement rate limiting
4. Add comprehensive error handling
5. Write integration tests
6. Add security testing
7. Optimize performance (caching, indexing)
8. Add monitoring and logging

---

## Resources

- [Cohere API Documentation](https://docs.cohere.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com)
