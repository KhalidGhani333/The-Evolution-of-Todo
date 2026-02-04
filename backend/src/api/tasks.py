"""
Tasks API endpoints.
Handles CRUD operations for tasks with JWT authentication and user isolation.
"""
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List, Optional
from src.database import get_session
from src.auth.jwt import verify_token, verify_user_access
from src.models.task import Task, TaskCreate, TaskUpdate, TaskResponse, TaskCompleteRequest
from src.services.task_service import TaskService

router = APIRouter()


@router.post("/api/{user_id}/tasks", response_model=TaskResponse, status_code=201)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    authenticated_user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Requires JWT authentication.
    User can only create tasks for themselves.
    """
    # Verify user can only create tasks for themselves
    verify_user_access(user_id, authenticated_user_id)

    # Create task
    task = TaskService.create_task(session, user_id, task_data)
    return task


@router.get("/api/{user_id}/tasks", response_model=dict)
async def get_tasks(
    user_id: str,
    status: Optional[str] = Query(None, description="Filter by status: all, pending, completed"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in title or description"),
    authenticated_user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user with optional filters.

    Requires JWT authentication.
    User can only view their own tasks.
    """
    # Verify user can only access their own tasks
    verify_user_access(user_id, authenticated_user_id)

    # Get tasks with filters
    tasks = TaskService.get_tasks(session, user_id, status, category, search)

    return {
        "tasks": tasks,
        "total": len(tasks),
        "filters": {
            "status": status,
            "category": category,
            "search": search
        }
    }


@router.get("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    authenticated_user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.

    Requires JWT authentication.
    User can only view their own tasks.
    """
    # Verify user can only access their own tasks
    verify_user_access(user_id, authenticated_user_id)

    # Get task (service handles user isolation)
    task = TaskService.get_task(session, user_id, task_id)
    return task


@router.put("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    authenticated_user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Update a task.

    Requires JWT authentication.
    User can only update their own tasks.
    """
    # Verify user can only update their own tasks
    verify_user_access(user_id, authenticated_user_id)

    # Update task (service handles user isolation)
    task = TaskService.update_task(session, user_id, task_id, task_data)
    return task


@router.delete("/api/{user_id}/tasks/{task_id}", status_code=204)
async def delete_task(
    user_id: str,
    task_id: int,
    authenticated_user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Delete a task.

    Requires JWT authentication.
    User can only delete their own tasks.
    """
    # Verify user can only delete their own tasks
    verify_user_access(user_id, authenticated_user_id)

    # Delete task (service handles user isolation)
    TaskService.delete_task(session, user_id, task_id)
    return None


@router.patch("/api/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str,
    task_id: int,
    request: TaskCompleteRequest,
    authenticated_user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status.

    Requires JWT authentication.
    User can only modify their own tasks.
    """
    # Verify user can only modify their own tasks
    verify_user_access(user_id, authenticated_user_id)

    # Toggle completion (service handles user isolation)
    task = TaskService.toggle_complete(session, user_id, task_id, request.completed)
    return task
