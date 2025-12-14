import sys
from typing import List

from sqlmodel import SQLModel

# Import models here to ensure they are available for create_all
# This import path assumes backend/src/models/__init__.py exports User and Todo
try:
    from .models import User, Todo
    MODELS_AVAILABLE = True
except ImportError:
    print("Warning: Could not import User and Todo models. Database setup might fail.")
    MODELS_AVAILABLE = False

def create_db_and_tables():
    """
    Creates all database tables defined by SQLModel metadata.
    This function is intended to be called during application startup or for setup.
    It ensures that the database schema matches the defined SQLModel classes.
    """
    if not MODELS_AVAILABLE:
        print("Error: Models are not available. Cannot create database tables.")
        sys.exit(1) # Exit if models cannot be imported, as DB setup would fail

    try:
        # Import the engine from the database module
        from .database import engine

        print("Attempting to create database tables...")
        # SQLModel.metadata.create_all(engine) creates all tables defined in the metadata
        SQLModel.metadata.create_all(engine)
        print("Database tables created or already exist successfully.")
    except ImportError:
        print("Error: Could not import 'engine' from backend.src.database.")
        print("Please ensure backend/src/database.py is correctly implemented.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during database table creation: {e}")
        # In a production environment, extensive logging should be implemented here.
        sys.exit(1)

if __name__ == "__main__":
    # This allows running the script directly for database setup
    # Example usage: python -m backend.src.database_setup create_all
    # Note: Running this directly might require setting up environment variables.
    
    if len(sys.argv) > 1 and sys.argv[1] == "create_all":
        create_db_and_tables()
    else:
        print("Usage: python -m backend.src.database_setup create_all")
