"""
Auth initialization package.
"""
from src.auth.jwt import verify_token

# Export verify_token as get_current_user for consistency
get_current_user = verify_token

__all__ = ['verify_token', 'get_current_user']
