# Data Model: AI-Powered Todo Chatbot

**Feature**: Phase III - AI Chatbot Integration
**Created**: 2026-02-06
**Status**: Design Complete

## Overview

This document defines the data model for the AI chatbot feature, including new entities for conversation management and their relationships with existing Phase II entities.

---

## Entity Definitions

### 1. Conversation

**Purpose**: Represents a chat thread between a user and the AI assistant.

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier for the conversation
- `user_id` (String, Foreign Key → users.id, Required, Indexed): Owner of the conversation
- `title` (String, Max 200, Default "New Conversation"): Human-readable conversation title
- `status` (Enum: active/archived, Default active, Indexed): Conversation lifecycle status
- `created_at` (Timestamp, Indexed): When conversation was created
- `updated_at` (Timestamp): Last activity timestamp

**Relationships**:
- One-to-Many with Message (conversation has many messages)
- Many-to-One with User (user has many conversations)

**Validation Rules**:
- user_id must reference existing user
- title cannot be empty
- status must be 'active' or 'archived'
- created_at cannot be in the future
- updated_at must be >= created_at

**State Transitions**:
- New → Active (on creation)
- Active → Archived (user archives or after 90 days inactive)
- Archived → Active (user restores)

**Indexes**:
- Primary: id
- Foreign: user_id
- Composite: (user_id, created_at) for listing user's conversations by recency
- Single: status for filtering active/archived

---

### 2. Message

**Purpose**: Represents a single message in a conversation (user or assistant).

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier for the message
- `conversation_id` (UUID, Foreign Key → conversations.id, Required, Indexed): Parent conversation
- `role` (Enum: user/assistant, Required, Indexed): Who sent the message
- `content` (Text, Required): Message text content
- `tool_calls` (JSON, Optional): Metadata about AI tool invocations (if role=assistant)
- `tool_results` (JSON, Optional): Results from tool executions (if role=assistant)
- `created_at` (Timestamp, Indexed): When message was created

**Relationships**:
- Many-to-One with Conversation (message belongs to one conversation)
- One-to-Many with ToolCall (optional, if using separate tool_calls table)

**Validation Rules**:
- conversation_id must reference existing conversation
- role must be 'user' or 'assistant'
- content cannot be empty
- content max length: 10,000 characters (to accommodate long AI responses)
- tool_calls and tool_results only valid when role='assistant'
- created_at cannot be in the future

**Indexes**:
- Primary: id
- Foreign: conversation_id
- Composite: (conversation_id, created_at) for retrieving messages in chronological order
- Single: role for filtering by message type

---

### 3. ToolCall (Optional)

**Purpose**: Detailed audit trail of AI tool invocations for debugging and analytics.

**Attributes**:
- `id` (UUID, Primary Key): Unique identifier for the tool call
- `message_id` (UUID, Foreign Key → messages.id, Required, Indexed): Associated message
- `tool_name` (String, Max 100, Required, Indexed): Name of tool invoked
- `parameters` (JSON, Required): Input parameters passed to tool
- `result` (JSON, Required): Output returned by tool
- `success` (Boolean, Required, Indexed): Whether tool execution succeeded
- `error_message` (Text, Optional): Error details if success=false
- `execution_time_ms` (Integer, Optional): Tool execution duration in milliseconds
- `created_at` (Timestamp, Indexed): When tool was invoked

**Relationships**:
- Many-to-One with Message (tool call belongs to one message)

**Validation Rules**:
- message_id must reference existing message with role='assistant'
- tool_name must be one of: add_task, list_tasks, complete_task, delete_task, update_task
- parameters must be valid JSON
- result must be valid JSON
- execution_time_ms must be >= 0 if provided
- created_at cannot be in the future

**Indexes**:
- Primary: id
- Foreign: message_id
- Single: tool_name for analytics on tool usage
- Single: success for monitoring failure rates
- Single: created_at for time-series analysis

---

## Existing Entities (Phase II)

### 4. User (Existing)

**Attributes** (relevant to Phase III):
- `id` (String, Primary Key): User identifier
- `email` (String, Unique): User email
- `created_at` (Timestamp): Account creation date

**New Relationships**:
- One-to-Many with Conversation (user has many conversations)

---

### 5. Task (Existing)

**Attributes** (unchanged):
- `id` (Integer, Primary Key): Task identifier
- `user_id` (String, Foreign Key → users.id): Task owner
- `title` (String): Task title
- `description` (Text, Optional): Task description
- `category` (String, Optional): Task category
- `completed` (Boolean): Completion status
- `created_at` (Timestamp): Creation date
- `updated_at` (Timestamp): Last modification date

**Relationships** (unchanged):
- Many-to-One with User (task belongs to one user)

**Note**: Tasks are accessed through AI tool functions but have no direct relationship with Conversation or Message entities.

---

## Entity Relationship Diagram

```
User (existing)
├── id (PK)
├── email
└── created_at
    │
    ├─── (1:N) ──→ Conversation
    │                ├── id (PK)
    │                ├── user_id (FK)
    │                ├── title
    │                ├── status
    │                ├── created_at
    │                └── updated_at
    │                    │
    │                    └─── (1:N) ──→ Message
    │                                    ├── id (PK)
    │                                    ├── conversation_id (FK)
    │                                    ├── role
    │                                    ├── content
    │                                    ├── tool_calls (JSON)
    │                                    ├── tool_results (JSON)
    │                                    └── created_at
    │                                        │
    │                                        └─── (1:N) ──→ ToolCall (optional)
    │                                                        ├── id (PK)
    │                                                        ├── message_id (FK)
    │                                                        ├── tool_name
    │                                                        ├── parameters (JSON)
    │                                                        ├── result (JSON)
    │                                                        ├── success
    │                                                        ├── error_message
    │                                                        ├── execution_time_ms
    │                                                        └── created_at
    │
    └─── (1:N) ──→ Task (existing)
                    ├── id (PK)
                    ├── user_id (FK)
                    ├── title
                    ├── description
                    ├── category
                    ├── completed
                    ├── created_at
                    └── updated_at
```

---

## Data Access Patterns

### Pattern 1: List User's Conversations
```sql
SELECT * FROM conversations
WHERE user_id = :user_id
ORDER BY updated_at DESC
LIMIT 20;
```
**Index Used**: (user_id, updated_at)

### Pattern 2: Get Conversation History
```sql
SELECT * FROM messages
WHERE conversation_id = :conversation_id
ORDER BY created_at ASC
LIMIT 50;
```
**Index Used**: (conversation_id, created_at)

### Pattern 3: Verify Conversation Ownership
```sql
SELECT id FROM conversations
WHERE id = :conversation_id AND user_id = :user_id;
```
**Index Used**: Primary key + user_id index

### Pattern 4: Create New Message
```sql
INSERT INTO messages (id, conversation_id, role, content, created_at)
VALUES (:id, :conversation_id, :role, :content, NOW());

UPDATE conversations
SET updated_at = NOW()
WHERE id = :conversation_id;
```
**Indexes Used**: Primary keys

### Pattern 5: Tool Usage Analytics
```sql
SELECT tool_name, COUNT(*) as usage_count, AVG(execution_time_ms) as avg_time
FROM tool_calls
WHERE created_at >= :start_date
GROUP BY tool_name
ORDER BY usage_count DESC;
```
**Index Used**: (tool_name, created_at)

---

## Data Retention Policy

### Active Data
- **Conversations**: Kept indefinitely while status='active'
- **Messages**: Kept indefinitely (part of conversation history)
- **ToolCalls**: Kept for 90 days for debugging, then archived

### Archived Data
- **Conversations**: status='archived' after 90 days of inactivity
- **Messages**: Retained with archived conversations
- **ToolCalls**: Moved to cold storage after 90 days

### User Deletion
- When user account deleted:
  - Cascade delete all conversations
  - Cascade delete all messages
  - Cascade delete all tool_calls
  - Soft delete tasks (mark as deleted, retain for 30 days)

---

## Migration Strategy

### Step 1: Create New Tables
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

-- Create tool_calls table (optional)
CREATE TABLE tool_calls (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
    tool_name VARCHAR(100) NOT NULL,
    parameters JSONB NOT NULL,
    result JSONB NOT NULL,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### Step 2: Create Indexes
```sql
-- Conversations indexes
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);
CREATE INDEX idx_conversations_user_created ON conversations(user_id, created_at);

-- Messages indexes
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_role ON messages(role);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);

-- Tool calls indexes (optional)
CREATE INDEX idx_tool_calls_message_id ON tool_calls(message_id);
CREATE INDEX idx_tool_calls_tool_name ON tool_calls(tool_name);
CREATE INDEX idx_tool_calls_success ON tool_calls(success);
CREATE INDEX idx_tool_calls_created_at ON tool_calls(created_at);
```

### Step 3: Verify Migration
- Check table creation
- Verify foreign key constraints
- Test index performance
- Validate data types and constraints

---

## SQLModel Implementation

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
    tool_calls: Optional[str] = Field(default=None)  # JSON string
    tool_results: Optional[str] = Field(default=None)  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    conversation: Conversation = Relationship(back_populates="messages")
    tool_call_records: List["ToolCall"] = Relationship(back_populates="message")

class ToolCall(SQLModel, table=True):
    __tablename__ = "tool_calls"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    message_id: str = Field(foreign_key="messages.id", nullable=False, index=True)
    tool_name: str = Field(nullable=False, max_length=100, index=True)
    parameters: str = Field(nullable=False)  # JSON string
    result: str = Field(nullable=False)  # JSON string
    success: bool = Field(nullable=False, index=True)
    error_message: Optional[str] = Field(default=None)
    execution_time_ms: Optional[int] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    message: Message = Relationship(back_populates="tool_call_records")
```

---

## Conclusion

This data model provides a solid foundation for conversation management with proper user isolation, audit trails, and performance optimization through strategic indexing. The schema is normalized, scalable, and follows Phase II conventions for consistency.
