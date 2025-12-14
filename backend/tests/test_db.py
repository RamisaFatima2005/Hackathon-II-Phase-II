import pytest
from sqlmodel import Session, SQLModel, create_engine, select
from datetime import datetime, timedelta
import os

# --- Imports ---
# Assuming models and database utilities are accessible from backend.src
try:
    from backend.src.models import User, Todo
    from backend.src.database import engine, get_session, create_db_and_tables, test_connection
    from backend.src.database_setup import create_db_and_tables as setup_tables # Alias to avoid name clash if needed
except ImportError as e:
    pytest.skip(f"Could not import necessary modules for database tests: {e}. Ensure backend.src is in PYTHONPATH.", allow_module_level=True)

# --- Configuration ---
# Use environment variables for database connection details, especially for testing.
# Fallback mechanisms or specific test DB URLs could be implemented here.
# For simplicity, we rely on the engine and get_session from database.py
# which should be configured via DATABASE_URL env var.

# --- Test Setup ---
# Pytest fixtures are assumed to be available from a conftest.py or other modules.
# We will use the 'engine' and 'db_session' fixtures defined in test_database_connection.py
# for managing the database connection and session scope.

# --- Test Cases for Database Operations ---

def test_db_connection_and_initialization(engine):
    """
    Tests the database connection and initialization process.
    This simulates calling test_connection() and create_db_and_tables().
    """
    print("\n--- Testing Database Connection and Initialization ---")
    
    # 1. Test Connection
    print("Running test_connection()...")
    connection_ok = test_connection()
    assert connection_ok, "Database connection test failed."
    print("test_connection() completed successfully.")

    # 2. Initialize Database (create tables)
    print("Running create_db_and_tables()...")
    try:
        # We expect create_db_and_tables to run without errors.
        # In a real test suite, you might want to ensure tables are truly created
        # or handle idempotency gracefully.
        setup_tables() 
        print("create_db_and_tables() completed successfully.")
        
        # Optional: Verify tables exist using the engine directly if needed,
        # but test_tables_are_created in test_database_connection.py likely covers this.
        from sqlalchemy import inspect
        inspector = inspect(engine)
        assert "user" in inspector.get_table_names(), "User table not found after initialization."
        assert "todo" in inspector.get_table_names(), "Todo table not found after initialization."
        print("Database tables (User, Todo) verified after initialization.")
        
    except Exception as e:
        pytest.fail(f"create_db_and_tables() failed during execution: {e}")
    print("--- Database Connection and Initialization Test Complete ---")

def test_crud_operations_with_users_and_todos(db_session: Session):
    """
    Tests Create, Read, Update, Delete operations for Users and Todos,
    ensuring user isolation is maintained throughout.
    """
    print("\n--- Testing CRUD Operations with Users and Todos ---")

    # --- 3. Create Test Users ---
    print("Creating test users...")
    user1_email = "db_test_user1@example.com"
    user2_email = "db_test_user2@example.com"
    user1_password_hash = "hashed_pw_user1"
    user2_password_hash = "hashed_pw_user2"

    user1 = User(email=user1_email, password_hash=user1_password_hash)
    user2 = User(email=user2_email, password_hash=user2_password_hash)
    
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()
    
    db_session.refresh(user1)
    db_session.refresh(user2)
    
    user1_id = user1.id
    user2_id = user2.id
    
    assert user1_id is not None
    assert user2_id is not None
    print(f"Test users created with IDs: User1={user1_id}, User2={user2_id}")

    # --- 4. Create Todos ---
    print("Creating todos for test users...")
    todos_user1_data = [
        {"title": "User1 Todo 1", "description": "Buy milk", "completed": False},
        {"title": "User1 Todo 2", "description": "Walk dog", "completed": True},
        {"title": "User1 Todo 3", "description": "Read book", "completed": False},
    ]
    todos_user2_data = [
        {"title": "User2 Todo A", "description": "Pay bills", "completed": False},
        {"title": "User2 Todo B", "description": "Schedule appointment", "completed": False},
    ]

    created_todos_user1 = []
    for data in todos_user1_data:
        todo = Todo(user_id=user1_id, **data)
        db_session.add(todo)
        created_todos_user1.append(todo)
    
    created_todos_user2 = []
    # Correcting the typo: should be todo, not todo_to_delete
    for data in todos_user2_data:
        todo = Todo(user_id=user2_id, **data)
        db_session.add(todo)
        created_todos_user2.append(todo)

    db_session.commit()
    
    # Refresh to get IDs and potentially default 'created_at'
    for todo in created_todos_user1:
        db_session.session.refresh(todo)
    for todo in created_todos_user2:
        db_session.session.refresh(todo)

    print(f"Created {len(created_todos_user1)} todos for User1 and {len(created_todos_user2)} for User2.")

    # --- 5. Test Read Operations (Verify Isolation) ---
    print("Testing read operations and user isolation...")
    
    # Query all todos for user1
    user1_todos_db = db_session.query(Todo).filter(Todo.user_id == user1_id).all()
    assert len(user1_todos_db) == 3, f"Expected 3 todos for User1, found {len(user1_todos_db)}"
    assert {{t.title for t in user1_todos_db}} == {"User1 Todo 1", "User1 Todo 2", "User1 Todo 3"}
    print(f"Successfully read {len(user1_todos_db)} todos for User1.")

    # Query all todos for user2
    user2_todos_db = db_session.query(Todo).filter(Todo.user_id == user2_id).all()
    assert len(user2_todos_db) == 2, f"Expected 2 todos for User2, found {len(user2_todos_db)}"
    assert {{t.title for t in user2_todos_db}} == {"User2 Todo A", "User2 Todo B"}
    print(f"Successfully read {len(user2_todos_db)} todos for User2.")
    print("User isolation for read operations verified.")

    # --- 6. Test Update ---
    print("Testing update operations...")
    # Update User1's first todo
    todo_to_update = db_session.query(Todo).filter(Todo.user_id == user1_id, Todo.title == "User1 Todo 1").first()
    assert todo_to_update is not None, "Todo item for update not found for User1."
    
    original_title = todo_to_update.title
    updated_title = "Updated Grocery List"
    updated_description = "Milk, Bread, Eggs, Cheese"
    updated_completed_status = True
    
    todo_to_update.title = updated_title
    todo_to_update.description = updated_description
    todo_to_update.completed = updated_completed_status
    
    db_session.add(todo_to_update)
    db_session.commit()
    db_session.refresh(todo_to_update)
    
    assert todo_to_update.title == updated_title
    assert todo_to_update.description == updated_description
    assert todo_to_update.completed == updated_completed_status
    print(f"Todo updated: {todo_to_update}")
    print("Update operation verified.")

    # --- 7. Test Delete ---
    print("Testing delete operations...")
    # Delete one todo from User 1
    todo_to_delete_user1 = db_session.query(Todo).filter(Todo.user_id == user1_id, Todo.title == "User1 Todo 3").first()
    assert todo_to_delete_user1 is not None, "Todo item for deletion not found for User1."
    
    todo_id_to_delete = todo_to_delete_user1.id
    db_session.delete(todo_to_delete_user1)
    db_session.commit()
    
    # Verify deletion for User 1
    deleted_todo = db_session.query(Todo).filter(Todo.id == todo_id_to_delete).first()
    assert deleted_todo is None, f"Todo item with ID {todo_id_to_delete} was not deleted."
    print(f"Todo with ID {todo_id_to_delete} deleted successfully.")
    
    # Verify User 1's remaining todos count
    user1_remaining_todos = db_session.query(Todo).filter(Todo.user_id == user1_id).all()
    assert len(user1_remaining_todos) == 2, f"Expected 2 remaining todos for User1, found {len(user1_todos_db) - 1}"
    print(f"User1 has {len(user1_remaining_todos)} todos remaining after deletion.")
    
    # Verify User 2's todos are unaffected
    user2_todos_after_delete = db_session.query(Todo).filter(Todo.user_id == user2_id).all()
    assert len(user2_todos_after_delete) == 2, f"User2's todos count changed after User1's deletion. Expected 2, found {len(user2_todos_after_delete)}"
    print("User isolation for delete operation verified.")
    print("--- CRUD Operations Test Complete ---")
