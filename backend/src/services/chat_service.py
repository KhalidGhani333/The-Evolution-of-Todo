"""
Chat service for AI-powered conversational interface.

This module handles Cohere API integration, conversation management,
and tool calling orchestration for the AI chatbot feature.
"""

import cohere
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlmodel import Session, select
from src.models.conversation import Conversation, Message, MessageRole, ConversationStatus
from src.services.chat_tools import ChatTools
from fastapi import HTTPException
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class ChatService:
    """Service for managing AI chat interactions."""

    def __init__(self):
        """Initialize ChatService with Cohere client and tool definitions."""
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")

        self.co = cohere.Client(api_key=api_key)
        self.tools = self._define_tools()
        self.history_limit = int(os.getenv("CHAT_HISTORY_LIMIT", "50"))

    def _define_tools(self) -> List[Dict]:
        """
        Define Cohere tool schemas for task management.

        Returns:
            List of tool definitions with parameter schemas
        """
        return [
            {
                "name": "add_task",
                "description": "Create a new task for the user",
                "parameter_definitions": {
                    "title": {
                        "description": "The title of the task",
                        "type": "str",
                        "required": True
                    },
                    "description": {
                        "description": "Optional detailed description of the task",
                        "type": "str",
                        "required": False
                    },
                    "category": {
                        "description": "Optional category for organizing the task",
                        "type": "str",
                        "required": False
                    }
                }
            },
            {
                "name": "list_tasks",
                "description": "Retrieve all tasks for the user with optional filters",
                "parameter_definitions": {
                    "status": {
                        "description": "Filter by status: 'all', 'pending', or 'completed'",
                        "type": "str",
                        "required": False
                    },
                    "category": {
                        "description": "Filter by category name",
                        "type": "str",
                        "required": False
                    }
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameter_definitions": {
                    "task_id": {
                        "description": "The ID of the task to complete",
                        "type": "int",
                        "required": True
                    }
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task permanently",
                "parameter_definitions": {
                    "task_id": {
                        "description": "The ID of the task to delete",
                        "type": "int",
                        "required": True
                    }
                }
            },
            {
                "name": "update_task",
                "description": "Update properties of an existing task",
                "parameter_definitions": {
                    "task_id": {
                        "description": "The ID of the task to update",
                        "type": "int",
                        "required": True
                    },
                    "title": {
                        "description": "New title for the task",
                        "type": "str",
                        "required": False
                    },
                    "description": {
                        "description": "New description for the task",
                        "type": "str",
                        "required": False
                    },
                    "category": {
                        "description": "New category for the task",
                        "type": "str",
                        "required": False
                    }
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
        """
        Process chat message and return AI response.

        Args:
            session: Database session
            user_id: Authenticated user ID
            message: User's message text
            conversation_id: Existing conversation ID (optional)

        Returns:
            Dict with conversation_id and AI response message

        Raises:
            HTTPException: If conversation not found or API error
        """
        logger.info(f"Chat request - user_id: {user_id}, conversation_id: {conversation_id}, message_length: {len(message)}")

        try:
            # Get or create conversation
            if conversation_id:
                conversation = self._get_conversation(session, user_id, conversation_id)
                logger.debug(f"Retrieved existing conversation: {conversation_id}")
            else:
                conversation = self._create_conversation(session, user_id)
                logger.info(f"Created new conversation: {conversation.id} for user: {user_id}")

            # Get conversation history
            chat_history = self._get_chat_history(session, conversation.id)
            logger.debug(f"Loaded {len(chat_history)} messages from history")

            # Call Cohere API
            logger.debug(f"Calling Cohere API with {len(self.tools)} tools")
            response = self.co.chat(
                model="command-r-08-2024",
                message=message,
                chat_history=chat_history,
                tools=self.tools,
                temperature=0.3
            )

            # Handle tool calls if any
            if response.tool_calls:
                logger.info(f"AI requested {len(response.tool_calls)} tool calls")
                for tool_call in response.tool_calls:
                    logger.debug(f"Tool call: {tool_call.name} with params: {tool_call.parameters}")

                tool_results = self._execute_tools(session, user_id, response.tool_calls)

                # Get final response with tool results
                # Must include both user message AND chatbot response in history
                # so that last entry is CHATBOT (required by Cohere when sending tool_results)
                final_response = self.co.chat(
                    model="command-r-08-2024",
                    message="",
                    chat_history=chat_history + [
                        {"role": "USER", "message": message},
                        {"role": "CHATBOT", "message": response.text}
                    ],
                    tools=self.tools,
                    tool_results=tool_results
                )

                assistant_message = final_response.text
                logger.info(f"AI response with tool results - length: {len(assistant_message)}")
            else:
                assistant_message = response.text
                logger.info(f"AI response without tools - length: {len(assistant_message)}")

            # Save messages to database
            self._save_message(session, conversation.id, "user", message)
            self._save_message(session, conversation.id, "assistant", assistant_message)
            logger.debug(f"Saved messages to conversation: {conversation.id}")

            # Auto-generate title from first message if still default
            if conversation.title == "New Conversation":
                conversation.title = self._generate_title(message)
                logger.debug(f"Generated conversation title: {conversation.title}")

            # Update conversation timestamp
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()

            logger.info(f"Chat completed successfully - conversation_id: {conversation.id}")
            return {
                "conversation_id": str(conversation.id),  # Convert UUID to string
                "message": assistant_message
            }

        except (cohere.UnauthorizedError, cohere.ForbiddenError) as e:
            logger.error(f"Cohere authentication error: {e}")
            raise HTTPException(status_code=500, detail="AI service authentication failed")
        except cohere.TooManyRequestsError as e:
            logger.error(f"Cohere rate limit error: {e}")
            raise HTTPException(status_code=429, detail="AI service rate limit exceeded")
        except (cohere.InternalServerError, cohere.ServiceUnavailableError, cohere.GatewayTimeoutError) as e:
            logger.error(f"Cohere service error: {e}")
            raise HTTPException(status_code=503, detail="AI service temporarily unavailable")
        except Exception as e:
            logger.error(f"Chat error: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

    def _get_conversation(
        self,
        session: Session,
        user_id: str,
        conversation_id: str
    ) -> Conversation:
        """
        Retrieve existing conversation with user isolation.

        Args:
            session: Database session
            user_id: Authenticated user ID
            conversation_id: Conversation ID to retrieve

        Returns:
            Conversation object

        Raises:
            HTTPException: If conversation not found or access denied
        """
        conversation = session.exec(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
        ).first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return conversation

    def _create_conversation(
        self,
        session: Session,
        user_id: str
    ) -> Conversation:
        """
        Create new conversation for user.

        Args:
            session: Database session
            user_id: Authenticated user ID

        Returns:
            New Conversation object
        """
        conversation = Conversation(
            user_id=user_id,
            title="New Conversation",
            status="active",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        return conversation

    def _get_chat_history(
        self,
        session: Session,
        conversation_id: str
    ) -> List[Dict]:
        """
        Fetch last N messages in Cohere format.

        Args:
            session: Database session
            conversation_id: Conversation ID

        Returns:
            List of messages in Cohere chat_history format
        """
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(self.history_limit)
        ).all()

        # Transform to Cohere format
        chat_history = []
        for msg in messages:
            chat_history.append({
                "role": "USER" if msg.role == "user" else "CHATBOT",
                "message": msg.content
            })

        return chat_history

    def _save_message(
        self,
        session: Session,
        conversation_id: str,
        role: MessageRole,
        content: str
    ) -> Message:
        """
        Persist message to database.

        Args:
            session: Database session
            conversation_id: Parent conversation ID
            role: Message role (user or assistant)
            content: Message text

        Returns:
            Saved Message object
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )

        session.add(message)
        session.commit()
        session.refresh(message)

        return message

    def _generate_title(self, message: str) -> str:
        """
        Generate a conversation title from the first message.

        Args:
            message: First user message

        Returns:
            Concise title (max 50 characters)
        """
        # Clean up the message
        title = ' '.join(message.split())

        # Truncate to 50 characters
        if len(title) > 50:
            title = title[:47] + "..."

        return title

    def _execute_tools(
        self,
        session: Session,
        user_id: str,
        tool_calls: List
    ) -> List[Dict]:
        """
        Execute tool calls and return results.

        Args:
            session: Database session
            user_id: Authenticated user ID
            tool_calls: List of tool calls from Cohere

        Returns:
            List of tool results in Cohere format
        """
        results = []
        for tool_call in tool_calls:
            result = ChatTools.execute_tool(
                tool_name=tool_call.name,
                parameters=tool_call.parameters,
                user_id=user_id,
                session=session
            )
            results.append({
                "call": {
                    "name": tool_call.name,
                    "parameters": tool_call.parameters
                },
                "outputs": [result]
            })
        return results
