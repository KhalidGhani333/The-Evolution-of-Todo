"""
Chat API endpoints for AI-powered conversational interface.

This module provides REST API endpoints for chat functionality,
including sending messages and managing conversations.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel import Session, select
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from src.database import get_session
from src.auth import get_current_user
from src.services.chat_service import ChatService
from src.models.conversation import Conversation, Message
import logging
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize chat service
chat_service = ChatService()

# Simple in-memory rate limiter
# In production, use Redis or similar distributed cache
rate_limit_store = defaultdict(list)
RATE_LIMIT_REQUESTS = 60  # requests per window
RATE_LIMIT_WINDOW = 60  # seconds


def check_rate_limit(user_id: str) -> bool:
    """
    Check if user has exceeded rate limit.

    Args:
        user_id: User ID to check

    Returns:
        True if within limit, False if exceeded
    """
    now = datetime.utcnow()
    window_start = now - timedelta(seconds=RATE_LIMIT_WINDOW)

    # Clean old requests
    rate_limit_store[user_id] = [
        req_time for req_time in rate_limit_store[user_id]
        if req_time > window_start
    ]

    # Check limit
    if len(rate_limit_store[user_id]) >= RATE_LIMIT_REQUESTS:
        return False

    # Add current request
    rate_limit_store[user_id].append(now)
    return True


class ChatRequest(BaseModel):
    """Request schema for chat messages."""
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None

    @validator('message')
    def validate_message(cls, v):
        """Validate message content."""
        # Remove excessive whitespace
        v = ' '.join(v.split())

        # Check for empty after cleanup
        if not v.strip():
            raise ValueError("Message cannot be empty")

        # Check for suspicious patterns (basic prompt injection detection)
        suspicious_patterns = [
            "ignore previous instructions",
            "ignore all previous",
            "disregard previous",
            "forget previous",
            "new instructions:",
            "system:",
            "admin:",
            "root:",
        ]

        v_lower = v.lower()
        for pattern in suspicious_patterns:
            if pattern in v_lower:
                # Log security event
                logger.warning(
                    f"Suspicious pattern detected in message: '{pattern}' - "
                    f"Message preview: {v[:100]}..."
                )
                raise ValueError("Message contains suspicious content")

        return v


class ChatResponse(BaseModel):
    """Response schema for chat messages."""
    conversation_id: str
    message: str


class ConversationResponse(BaseModel):
    """Response schema for conversation metadata."""
    id: str
    title: str
    status: str
    created_at: str
    updated_at: str


class ConversationListResponse(BaseModel):
    """Response schema for conversation list."""
    conversations: List[ConversationResponse]
    total: int


class CreateConversationRequest(BaseModel):
    """Request schema for creating a conversation."""
    title: Optional[str] = "New Conversation"


class UpdateConversationRequest(BaseModel):
    """Request schema for updating a conversation."""
    title: Optional[str] = None
    status: Optional[str] = None


@router.post("", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Send a chat message and get AI response.

    Args:
        request: Chat request with message and optional conversation_id
        session: Database session (injected)
        user_id: Authenticated user ID (injected from JWT)

    Returns:
        ChatResponse with conversation_id and AI message

    Raises:
        HTTPException: 400 for invalid input, 404 for conversation not found,
                      429 for rate limit exceeded, 500 for server errors
    """
    # Check rate limit
    if not check_rate_limit(user_id):
        logger.warning(f"Rate limit exceeded for user: {user_id}")
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW} seconds."
        )

    try:
        response = chat_service.chat(
            session=session,
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id
        )
        return ChatResponse(**response)
    except HTTPException:
        # Re-raise HTTP exceptions from service layer
        raise
    except ValueError as e:
        # Validation errors
        logger.error(f"Validation error in send_message: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Unexpected errors
        logger.error(f"Unexpected error in send_message: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/conversations", response_model=ConversationListResponse)
async def list_conversations(
    status: Optional[str] = Query("active", pattern="^(active|archived|all)$"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    List user's conversations with pagination.

    Args:
        status: Filter by status (active, archived, all)
        limit: Maximum conversations to return
        offset: Number of conversations to skip
        session: Database session (injected)
        user_id: Authenticated user ID (injected)

    Returns:
        ConversationListResponse with conversations and total count
    """
    try:
        # Build query with user isolation
        query = select(Conversation).where(Conversation.user_id == user_id)

        # Apply status filter
        if status != "all":
            query = query.where(Conversation.status == status)

        # Order by most recent activity
        query = query.order_by(Conversation.updated_at.desc())

        # Get total count
        total_query = query
        total = len(session.exec(total_query).all())

        # Apply pagination
        query = query.offset(offset).limit(limit)
        conversations = session.exec(query).all()

        # Format response
        conversation_list = [
            ConversationResponse(
                id=conv.id,
                title=conv.title,
                status=conv.status,
                created_at=conv.created_at.isoformat(),
                updated_at=conv.updated_at.isoformat()
            )
            for conv in conversations
        ]

        return ConversationListResponse(
            conversations=conversation_list,
            total=total
        )
    except Exception as e:
        logger.error(f"Error listing conversations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    request: CreateConversationRequest,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Create a new conversation.

    Args:
        request: Conversation creation request
        session: Database session (injected)
        user_id: Authenticated user ID (injected)

    Returns:
        ConversationResponse with new conversation details
    """
    try:
        from datetime import datetime

        conversation = Conversation(
            user_id=user_id,
            title=request.title or "New Conversation",
            status="active",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        return ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            status=conversation.status.value,
            created_at=conversation.created_at.isoformat(),
            updated_at=conversation.updated_at.isoformat()
        )
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    limit: int = Query(50, ge=1, le=100),
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Get conversation details with message history.

    Args:
        conversation_id: Conversation ID
        limit: Maximum messages to return
        session: Database session (injected)
        user_id: Authenticated user ID (injected)

    Returns:
        Conversation details with messages

    Raises:
        HTTPException: 404 if conversation not found
    """
    try:
        # Get conversation with user isolation
        conversation = session.exec(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
        ).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Get messages
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        ).all()

        return {
            "id": conversation.id,
            "title": conversation.title,
            "status": conversation.status.value,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "created_at": msg.created_at.isoformat()
                }
                for msg in messages
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/conversations/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: str,
    request: UpdateConversationRequest,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Update conversation properties.

    Args:
        conversation_id: Conversation ID
        request: Update request with title and/or status
        session: Database session (injected)
        user_id: Authenticated user ID (injected)

    Returns:
        Updated conversation details

    Raises:
        HTTPException: 404 if conversation not found
    """
    try:
        from datetime import datetime

        # Get conversation with user isolation
        conversation = session.exec(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
        ).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Update fields
        if request.title is not None:
            conversation.title = request.title

        if request.status is not None:
            if request.status not in ["active", "archived"]:
                raise HTTPException(status_code=400, detail="Invalid status")
            conversation.status = request.status

        conversation.updated_at = datetime.utcnow()

        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        return ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            status=conversation.status.value,
            created_at=conversation.created_at.isoformat(),
            updated_at=conversation.updated_at.isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating conversation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/conversations/{conversation_id}", status_code=204)
async def delete_conversation(
    conversation_id: str,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user)
):
    """
    Delete a conversation and all its messages.

    Args:
        conversation_id: Conversation ID
        session: Database session (injected)
        user_id: Authenticated user ID (injected)

    Raises:
        HTTPException: 404 if conversation not found
    """
    try:
        # Get conversation with user isolation
        conversation = session.exec(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
        ).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Delete conversation (cascade will delete messages)
        session.delete(conversation)
        session.commit()

        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
