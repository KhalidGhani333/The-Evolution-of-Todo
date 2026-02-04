"""
Database initialization script.
Creates all tables with proper indexes.
"""
from src.database import create_db_and_tables
from src.models import User, Task

if __name__ == "__main__":
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully!")
    print("Tables: users, tasks")
    print("Indexes: user_id, completed, category on tasks table")
