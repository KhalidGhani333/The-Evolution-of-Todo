"""
JWT verification middleware for FastAPI.
Verifies JWT tokens issued by Better Auth.
"""
import os
from typing import Optional
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

# Security scheme
security = HTTPBearer()

# Get secret from environment
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
if not BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is not set")

ALGORITHM = "HS256"


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Verify JWT token and return user_id.

    Args:
        credentials: HTTP Authorization credentials with Bearer token

    Returns:
        user_id: The authenticated user's ID from token

    Raises:
        HTTPException: 401 if token is invalid or expired
    """
    token = credentials.credentials

    try:
        # Decode and verify JWT token
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: missing user ID"
            )

        return user_id

    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )


def verify_user_access(user_id_from_url: str, authenticated_user_id: str) -> None:
    """
    Verify that the authenticated user matches the user_id in the URL.

    Args:
        user_id_from_url: User ID from the URL path parameter
        authenticated_user_id: User ID from the verified JWT token

    Raises:
        HTTPException: 403 if user IDs don't match
    """
    if user_id_from_url != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Cannot access another user's data"
        )
