"""
Tasks API endpoints.
Handles CRUD operations for tasks with JWT authentication and user isolation.
"""
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List, Optional
from src.database import get_session
from src.auth.jwt import verify_token
from src.models.task import Task, TaskCreate, TaskUpdate, TaskResponse, TaskCompleteRequest
from src.services.task_service import TaskService

router = APIRouter()


@router.post("/api/tasks", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Requires JWT authentication.
    User ID is extracted from JWT token.
    """
    # Create task using authenticated user_id from JWT
    task = TaskService.create_task(session, user_id, task_data)
    return task


@router.get("/api/tasks", response_model=dict)
async def get_tasks(
    status: Optional[str] = Query(None, description="Filter by status: all, pending, completed"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in title or description"),
    user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user with optional filters.

    Requires JWT authentication.
    User ID is extracted from JWT token.
    """
    # Get tasks using authenticated user_id from JWT
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


@router.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.

    Requires JWT authentication.
    User ID is extracted from JWT token.
    """
    # Get task using authenticated user_id from JWT
    task = TaskService.get_task(session, user_id, task_id)
    return task


@router.patch("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Update a task.

    Requires JWT authentication.
    User ID is extracted from JWT token.
    """
    # Update task using authenticated user_id from JWT
    task = TaskService.update_task(session, user_id, task_id, task_data)
    return task


@router.delete("/api/tasks/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Delete a task.

    Requires JWT authentication.
    User ID is extracted from JWT token.
    """
    # Delete task using authenticated user_id from JWT
    TaskService.delete_task(session, user_id, task_id)
    return None


@router.post("/api/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    task_id: int,
    request: TaskCompleteRequest,
    user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status.

    Requires JWT authentication.
    User ID is extracted from JWT token.
    """
    # Toggle completion using authenticated user_id from JWT
    task = TaskService.toggle_complete(session, user_id, task_id, request.completed)
    return task
