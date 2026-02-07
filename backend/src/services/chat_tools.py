"""
Chat tools for AI-powered task management.

This module provides tool functions that the AI can invoke to perform
task operations. Each tool wraps existing TaskService methods with
user isolation and error handling.
"""

from typing import Dict, Any, Optional
from sqlmodel import Session
import logging

logger = logging.getLogger(__name__)


class ChatTools:
    """Tool functions for AI chat integration."""

    @staticmethod
    def execute_tool(
        tool_name: str,
        parameters: Dict[str, Any],
        user_id: str,
        session: Session
    ) -> Dict[str, Any]:
        """
        Route tool calls to appropriate tool functions.

        Args:
            tool_name: Name of tool to execute
            parameters: Tool parameters from AI
            user_id: Authenticated user ID
            session: Database session

        Returns:
            Tool execution result with success status and data/error
        """
        # Map tool names to functions
        tool_map = {
            "add_task": ChatTools.add_task,
            "list_tasks": ChatTools.list_tasks,
            "complete_task": ChatTools.complete_task,
            "delete_task": ChatTools.delete_task,
            "update_task": ChatTools.update_task
        }

        if tool_name not in tool_map:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

        try:
            # Execute tool with user_id and session injected
            result = tool_map[tool_name](
                session=session,
                user_id=user_id,
                **parameters
            )
            return result
        except Exception as e:
            logger.error(f"Tool execution error for {tool_name}: {e}")
            return {
                "success": False,
                "error": f"Tool execution failed: {str(e)}"
            }

    @staticmethod
    def add_task(
        session: Session,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new task for the user.

        Args:
            session: Database session
            user_id: Authenticated user ID
            title: Task title (required)
            description: Task description (optional)
            category: Task category (optional)

        Returns:
            Dict with success status and task data or error message
        """
        try:
            # Import here to avoid circular dependency
            from src.services.task_service import TaskService
            from src.models.task import TaskCreate

            task_data = TaskCreate(
                title=title,
                description=description,
                category=category
            )
            task = TaskService.create_task(session, user_id, task_data)

            return {
                "success": True,
                "message": f"Task '{task.title}' created successfully",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "category": task.category,
                    "completed": task.completed
                }
            }
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def list_tasks(
        session: Session,
        user_id: str,
        status: Optional[str] = None,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve all tasks for the user with optional filters.

        Args:
            session: Database session
            user_id: Authenticated user ID
            status: Filter by status ('all', 'pending', 'completed')
            category: Filter by category

        Returns:
            Dict with success status and list of tasks or error message
        """
        try:
            # Import here to avoid circular dependency
            from src.services.task_service import TaskService

            tasks = TaskService.get_tasks(session, user_id, status, category, None)

            task_list = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "category": task.category,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None
                }
                for task in tasks
            ]

            return {
                "success": True,
                "count": len(task_list),
                "tasks": task_list
            }
        except Exception as e:
            logger.error(f"Error listing tasks: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def complete_task(
        session: Session,
        user_id: str,
        task_id: int
    ) -> Dict[str, Any]:
        """
        Mark a task as completed.

        Args:
            session: Database session
            user_id: Authenticated user ID
            task_id: ID of task to complete

        Returns:
            Dict with success status and updated task or error message
        """
        try:
            # Import here to avoid circular dependency
            from src.services.task_service import TaskService

            task = TaskService.toggle_complete(session, user_id, task_id, True)

            return {
                "success": True,
                "message": f"Task '{task.title}' marked as completed",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.completed
                }
            }
        except Exception as e:
            logger.error(f"Error completing task: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def delete_task(
        session: Session,
        user_id: str,
        task_id: int
    ) -> Dict[str, Any]:
        """
        Delete a task permanently.

        Args:
            session: Database session
            user_id: Authenticated user ID
            task_id: ID of task to delete

        Returns:
            Dict with success status or error message
        """
        try:
            # Import here to avoid circular dependency
            from src.services.task_service import TaskService

            TaskService.delete_task(session, user_id, task_id)

            return {
                "success": True,
                "message": "Task deleted successfully"
            }
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def update_task(
        session: Session,
        user_id: str,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update properties of an existing task.

        Args:
            session: Database session
            user_id: Authenticated user ID
            task_id: ID of task to update
            title: New title (optional)
            description: New description (optional)
            category: New category (optional)

        Returns:
            Dict with success status and updated task or error message
        """
        try:
            # Import here to avoid circular dependency
            from src.services.task_service import TaskService
            from src.models.task import TaskUpdate

            task_data = TaskUpdate(
                title=title,
                description=description,
                category=category
            )
            task = TaskService.update_task(session, user_id, task_id, task_data)

            return {
                "success": True,
                "message": f"Task '{task.title}' updated successfully",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "category": task.category,
                    "completed": task.completed
                }
            }
        except Exception as e:
            logger.error(f"Error updating task: {e}")
            return {
                "success": False,
                "error": str(e)
            }
