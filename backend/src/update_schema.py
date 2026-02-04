"""
Update database schema to add hashed_password field to users table.
Run this after adding hashed_password to User model.
"""
from sqlmodel import create_engine, Session, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

engine = create_engine(DATABASE_URL, echo=True)

def update_schema():
    """Add hashed_password column to users table."""
    print("Updating database schema...")

    with Session(engine) as session:
        # Check if column exists
        check_query = text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='users' AND column_name='hashed_password'
        """)
        result = session.exec(check_query).first()

        if result:
            print("✓ hashed_password column already exists")
        else:
            # Add hashed_password column
            alter_query = text("""
                ALTER TABLE users
                ADD COLUMN hashed_password VARCHAR NOT NULL DEFAULT ''
            """)
            session.exec(alter_query)
            session.commit()
            print("✓ Added hashed_password column to users table")

    print("Schema update complete!")

if __name__ == "__main__":
    update_schema()
