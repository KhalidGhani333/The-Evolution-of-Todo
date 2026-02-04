"""
Authentication API endpoints.
Handles user signup, signin, and JWT token generation.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
import bcrypt
from datetime import datetime, timedelta
import jwt
import os
from src.database import get_session
from src.models.user import User

router = APIRouter()

# JWT settings
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-min-32-characters-long-for-security")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24 * 7  # 7 days


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None


class SigninRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    # Convert password to bytes and hash it
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a bcrypt hash."""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(user_id: str, email: str, name: str | None = None) -> str:
    """Create a JWT access token."""
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    payload = {
        "sub": user_id,
        "email": email,
        "name": name,
        "exp": expire
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


@router.post("/api/auth/signup", response_model=TokenResponse)
async def signup(
    request: SignupRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user and return a JWT token.

    - Validates email uniqueness
    - Hashes password
    - Creates user in database
    - Returns JWT token
    """
    # Check if user already exists
    statement = select(User).where(User.email == request.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate password length
    if len(request.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    # Create new user
    import uuid
    hashed_pwd = hash_password(request.password)

    user = User(
        id=str(uuid.uuid4()),
        email=request.email,
        name=request.name or "",
        hashed_password=hashed_pwd,
        email_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate JWT token
    token = create_access_token(user.id, user.email, user.name)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email
    )


@router.post("/api/auth/signin", response_model=TokenResponse)
async def signin(
    request: SigninRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return a JWT token.

    - Validates credentials
    - Returns JWT token
    """
    # Find user by email
    statement = select(User).where(User.email == request.email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Verify password
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT token
    token = create_access_token(user.id, user.email, user.name)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email
    )


@router.post("/api/auth/logout")
async def logout():
    """
    Logout endpoint (in a real app, you might blacklist the token).
    """
    return {"message": "Logged out successfully"}


@router.get("/api/auth/me")
async def get_current_user():
    """
    Get current user info from the token.
    """
    # This would require JWT verification middleware
    return {"message": "User info endpoint"}
