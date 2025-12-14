import os
from datetime import datetime
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel

# Load environment variables from .env file
# This is crucial for sensitive information like database URLs and secrets
load_dotenv()

# Retrieve database URL from environment variables
# Fallback to a default or raise an error if not found
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables. Please set it in your .env file.")

# Create the database engine
# echo=True is useful for debugging SQL queries during development
# pool_size and max_overflow configure connection pooling for better performance
# connect_args={"sslmode": "require"} is specific for Neon PostgreSQL to ensure SSL is used
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
    connect_args={"sslmode": "require"}
)


def create_db_and_tables():
    """
    Creates all database tables defined by SQLModel metadata.
    This function should be called once during application startup.
    """
    try:
        print("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        # In a real application, you might want more sophisticated error handling or logging
        raise


def get_session() -> Generator[Session, None, None]:
    """
    Provides a database session.

    This is a generator function that yields a new database session,
    ensuring it's properly closed after use. It's designed to be used
    with Python's 'with' statement.
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def test_connection() -> bool:
    """
    Tests the database connection by attempting to execute a simple query.
    Returns True if the connection is successful, False otherwise.
    """
    try:
        with get_session() as session:
            # Execute a simple query to verify connection
            # For PostgreSQL, 'SELECT 1' is a common way to test connection
            session.execute("SELECT 1")
            print("Database connection test successful.")
            return True
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False
