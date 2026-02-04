"""
Task model representing a todo item.
Each task belongs to a specific user with full data isolation.
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    """Task entity representing a todo item."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    category: Optional[str] = Field(default=None, max_length=50, index=True)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(SQLModel):
    """Schema for creating a new task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    category: Optional[str] = Field(default=None, max_length=50)


class TaskUpdate(SQLModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    category: Optional[str] = Field(default=None, max_length=50)


class TaskCompleteRequest(SQLModel):
    """Schema for toggling task completion status."""
    completed: bool


class TaskResponse(SQLModel):
    """Schema for task responses."""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    category: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
