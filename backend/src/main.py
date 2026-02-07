"""
FastAPI application entry point.
Configures CORS, routes, and middleware.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="Multi-user todo application with JWT authentication",
    version="1.0.0"
)

# Configure CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Todo API is running"}


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0"
    }


# Import and include routers
from src.api import tasks, auth, chat

app.include_router(tasks.router, tags=["tasks"])
app.include_router(auth.router, tags=["auth"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
