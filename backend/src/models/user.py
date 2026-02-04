"""
User model for Better Auth integration.
Represents an authenticated user with their own isolated task list.
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    """User entity managed by Better Auth."""
    __tablename__ = "users"

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, nullable=False, index=True)
    name: Optional[str] = Field(default=None, max_length=100)
    hashed_password: str = Field(nullable=False)  # Store hashed password
    email_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
