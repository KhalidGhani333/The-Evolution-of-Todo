"""
Conversation models for AI-powered chat functionality.

This module defines the database models for managing conversations,
messages, and tool call audit trails in the AI chatbot feature.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from enum import Enum
import uuid


class ConversationStatus(str, Enum):
    """Conversation status enumeration."""
    ACTIVE = "active"
    ARCHIVED = "archived"


class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"


class Conversation(SQLModel, table=True):
    """
    Conversation entity representing a chat thread.

    Attributes:
        id: Unique conversation identifier (UUID)
        user_id: Owner of the conversation (foreign key to users)
        title: Human-readable conversation title
        status: Conversation lifecycle status (active/archived)
        created_at: When conversation was created
        updated_at: Last activity timestamp
    """
    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(default="New Conversation", max_length=200)
    status: str = Field(default="active", index=True)  # Use string directly instead of enum
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """
    Message entity representing a single chat message.

    Attributes:
        id: Unique message identifier (UUID)
        conversation_id: Parent conversation (foreign key)
        role: Message sender (user or assistant)
        content: Message text content
        tool_calls: Optional metadata about AI tool invocations (JSON)
        tool_results: Optional results from tool executions (JSON)
        created_at: When message was created
    """
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", nullable=False, index=True)
    role: str = Field(nullable=False, index=True)  # Use string directly instead of enum
    content: str = Field(nullable=False, max_length=10000)
    tool_calls: Optional[str] = Field(default=None)  # JSON string
    tool_results: Optional[str] = Field(default=None)  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")

    # Relationship to tool call records
    tool_call_records: List["ToolCall"] = Relationship(back_populates="message")


class ToolCall(SQLModel, table=True):
    """
    Tool call entity for auditing AI function invocations.

    This optional table provides detailed audit trail of tool executions
    for debugging, analytics, and monitoring purposes.

    Attributes:
        id: Unique tool call identifier (UUID)
        message_id: Associated message (foreign key)
        tool_name: Name of tool invoked
        parameters: Input parameters (JSON)
        result: Output returned (JSON)
        success: Whether execution succeeded
        error_message: Error details if failed
        execution_time_ms: Execution duration in milliseconds
        created_at: When tool was invoked
    """
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

    # Relationship to message
    message: Message = Relationship(back_populates="tool_call_records")
