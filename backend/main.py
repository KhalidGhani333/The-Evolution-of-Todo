"""
Backend entry point - imports app from src.main
This allows running: uvicorn main:app from backend directory
"""
from src.main import app

__all__ = ["app"]

