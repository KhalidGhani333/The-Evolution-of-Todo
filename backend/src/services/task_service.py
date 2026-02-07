"""
Task service for CRUD operations.
Handles business logic and user isolation.
"""
from sqlmodel import Session, select
from datetime import datetime
from typing import List, Optional
from src.models.task import Task, TaskCreate, TaskUpdate
from fastapi import HTTPException


class TaskService:
    """Service for task operations with user isolation."""

    @staticmethod
    def create_task(
        session: Session,
        user_id: str,
        task_data: TaskCreate
    ) -> Task:
        """
        Create a new task for the authenticated user.

        Args:
            session: Database session
            user_id: Authenticated user's ID
            task_data: Task creation data

        Returns:
            Created task
        """
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            category=task_data.category,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_tasks(
        session: Session,
        user_id: str,
        status: Optional[str] = None,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Task]:
        """
        Get all tasks for the authenticated user with optional filters.

        Args:
            session: Database session
            user_id: Authenticated user's ID
            status: Filter by status (all, pending, completed)
            category: Filter by category
            search: Search keyword in title or description

        Returns:
            List of tasks matching filters
        """
        # Base query with user isolation
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "pending":
            query = query.where(Task.completed == False)

        # Apply category filter
        if category:
            query = query.where(Task.category == category)

        # Apply search filter
        if search:
            search_pattern = f"%{search.lower()}%"
            query = query.where(
                (Task.title.ilike(search_pattern)) |
                (Task.description.ilike(search_pattern))
            )

        # Order by created date (newest first)
        query = query.order_by(Task.created_at.desc())

        tasks = session.exec(query).all()
        return list(tasks)

    @staticmethod
    def get_task(
        session: Session,
        user_id: str,
        task_id: int
    ) -> Task:
        """
        Get a specific task by ID with user isolation.

        Args:
            session: Database session
            user_id: Authenticated user's ID
            task_id: Task ID

        Returns:
            Task if found and belongs to user

        Raises:
            HTTPException: 404 if task not found or doesn't belong to user
        """
        task = session.get(Task, task_id)

        if not task or task.user_id != user_id:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return task

    @staticmethod
    def update_task(
        session: Session,
        user_id: str,
        task_id: int,
        task_data: TaskUpdate
    ) -> Task:
        """
        Update a task with user isolation check.

        Args:
            session: Database session
            user_id: Authenticated user's ID
            task_id: Task ID
            task_data: Task update data

        Returns:
            Updated task

        Raises:
            HTTPException: 404 if task not found, 403 if not owned by user
        """
        task = session.get(Task, task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if task.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Forbidden: Cannot update another user's task"
            )

        # Update fields if provided
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.category is not None:
            task.category = task_data.category
        if task_data.completed is not None:
            task.completed = task_data.completed

        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(
        session: Session,
        user_id: str,
        task_id: int
    ) -> None:
        """
        Delete a task with user isolation check.

        Args:
            session: Database session
            user_id: Authenticated user's ID
            task_id: Task ID

        Raises:
            HTTPException: 404 if task not found, 403 if not owned by user
        """
        task = session.get(Task, task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if task.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Forbidden: Cannot delete another user's task"
            )

        session.delete(task)
        session.commit()

    @staticmethod
    def toggle_complete(
        session: Session,
        user_id: str,
        task_id: int,
        completed: bool
    ) -> Task:
        """
        Toggle task completion status with user isolation check.

        Args:
            session: Database session
            user_id: Authenticated user's ID
            task_id: Task ID
            completed: New completion status

        Returns:
            Updated task

        Raises:
            HTTPException: 404 if task not found, 403 if not owned by user
        """
        task = session.get(Task, task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if task.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Forbidden: Cannot modify another user's task"
            )

        task.completed = completed
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task
