import pytest
from sqlmodel import Session, SQLModel, create_engine
from datetime import datetime
from typing import List

# Assume backend/src/models/user.py, backend/src/models/todo.py, and backend/src/database.py are available
# Adjust imports as necessary based on your project structure and pytest setup
try:
    from backend.src.models import User, Todo
    from backend.src.database import engine, get_session # Import engine and session fixture if needed
except ImportError as e:
    pytest.skip(f"Could not import necessary modules for Todo model tests: {e}. Ensure backend.src is in PYTHONPATH.", allow_module_level=True)

# --- Test Setup ---
# We reuse the 'engine' and 'db_session' fixtures from test_database_connection.py
# assuming they are discoverable by pytest and correctly configured.

# --- Test Cases for Todo Model CRUD with User Isolation ---

def test_create_todo(db_session: Session):
    """
    Test creating a new todo item and associating it with a user.
    Verifies that basic creation and saving works.
    """
    # Create a user first, as Todo requires a valid user_id
    user = User(email="todo_create_user@example.com", password_hash="create_hash")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    user_id = user.id
    
    assert user_id is not None

    # Create a todo item for the user
    # Note: created_at defaults are handled by the model's default_factory
    todo = Todo(
        user_id=user_id,
        title="Buy groceries",
        description="Milk, Bread, Eggs",
        completed=False,
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    assert todo.id is not None
    assert todo.user_id == user_id
    assert todo.title == "Buy groceries"
    assert todo.description == "Milk, Bread, Eggs"
    assert todo.completed is False
    assert todo.created_at is not None # Check if datetime was assigned
    print(f"Todo created: {todo}")

def test_read_todos_for_user_isolation(db_session: Session):
    """
    Test retrieving all todo items for a specific user.
    Verifies that only the user's own todos are returned (user isolation).
    """
    # Create User 1 and their todos
    user1 = User(email="user1_todo_read@example.com", password_hash="hash1")
    db_session.add(user1)
    db_session.commit()
    db_session.refresh(user1)
    user1_id = user1.id

    todo1_user1 = Todo(user_id=user1_id, title="Task 1 for User 1")
    todo2_user1 = Todo(user_id=user1_id, title="Task 2 for User 1", completed=True)
    db_session.add(todo1_user1)
    db_session.add(todo2_user1)
    db_session.commit()

    # Create User 2 and their todo (to ensure isolation)
    user2 = User(email="user2_todo_read@example.com", password_hash="hash2")
    db_session.add(user2)
    db_session.commit()
    db_session.refresh(user2)
    user2_id = user2.id
    
    todo1_user2 = Todo(user_id=user2_id, title="Task for User 2")
    db_session.add(todo1_user2)
    db_session.commit()

    # Retrieve todos for User 1
    user1_todos = db_session.query(Todo).filter(Todo.user_id == user1_id).all()
    
    assert len(user1_todos) == 2
    assert {t.title for t in user1_todos} == {"Task 1 for User 1", "Task 2 for User 1"}
    print(f"Todos for User 1 retrieved: {user1_todos}")

    # Retrieve todos for User 2
    user2_todos = db_session.query(Todo).filter(Todo.user_id == user2_id).all()
    assert len(user2_todos) == 1
    assert user2_todos[0].title == "Task for User 2"
    print(f"Todos for User 2 retrieved: {user2_todos}")

def test_update_todo(db_session: Session):
    """
    Test updating an existing todo item's details.
    Verifies that changes are committed to the database.
    """
    # Create a user and a todo item
    user = User(email="update_todo_user@example.com", password_hash="update_hash")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    user_id = user.id

    todo_to_update = Todo(user_id=user_id, title="Old title", description="Old description", completed=False)
    db_session.add(todo_to_update)
    db_session.commit()
    db_session.refresh(todo_to_update)
    todo_id = todo_to_update.id

    # Update the todo item
    new_title = "New title"
    new_description = "New description"
    new_completed_status = True
    
    # Fetch the todo again to ensure we are working with the DB state
    fetched_todo = db_session.query(Todo).filter(Todo.id == todo_id).first()
    if fetched_todo:
        fetched_todo.title = new_title
        fetched_todo.description = new_description
        fetched_todo.completed = new_completed_status
        db_session.add(fetched_todo)
        db_session.commit()
        
        # Refresh to ensure changes are loaded from DB
        db_session.refresh(fetched_todo)
        
        assert fetched_todo.title == new_title
        assert fetched_todo.description == new_description
        assert fetched_todo.completed == new_completed_status
        print(f"Todo updated: {fetched_todo}")
    else:
        pytest.fail("Todo item not found for update.")

def test_delete_todo(db_session: Session):
    """
    Test deleting a todo item from the database.
    Verifies that the todo item is removed and user isolation is maintained.
    """
    # Create User 1 and their todo
    user1 = User(email="delete_todo_user1@example.com", password_hash="delete_hash1")
    db_session.add(user1)
    db_session.commit()
    db_session.refresh(user1)
    user1_id = user1.id

    todo_to_delete = Todo(user_id=user1_id, title="Task to be deleted")
    db_session.add(todo_to_delete)
    db_session.commit()
    db_session.refresh(todo_to_delete)
    todo_id_to_delete = todo_to_delete.id

    # Create User 2 and their todo (to ensure isolation)
    user2 = User(email="delete_todo_user2@example.com", password_hash="delete_hash2")
    db_session.add(user2)
    db_session.commit()
    db_session.refresh(user2)
    user2_id = user2.id
    
    todo_user2 = Todo(user_id=user2_id, title="Task not to be deleted")
    db_session.add(todo_user2)
    db_session.commit()

    # Delete the todo item belonging to User 1
    todo_for_deletion = db_session.query(Todo).filter(Todo.id == todo_id_to_delete).first()
    # Double-check ownership before deleting (crucial for isolation tests)
    if todo_for_deletion and todo_for_deletion.user_id == user1_id:
        db_session.delete(todo_for_deletion)
        db_session.commit()
        
        # Verify deletion for User 1
        deleted_todo = db_session.query(Todo).filter(Todo.id == todo_id_to_delete).first()
        assert deleted_todo is None
        print(f"Todo with ID {todo_id_to_delete} deleted successfully.")
        
        # Verify User 2's todo is still present
        user2_remaining_todos = db_session.query(Todo).filter(Todo.user_id == user2_id).all()
        assert len(user2_remaining_todos) == 1
        assert user2_remaining_todos[0].id == todo_user2.id # Ensure it's the correct todo
        print("User 2's todo item remains untouched.")
    else:
        pytest.fail(f"Todo item to delete (ID: {todo_id_to_delete}) not found or does not belong to user {user1_id}.")

def test_todo_title_length_constraint(db_session: Session):
    """
    Test that the title field adheres to its max_length and min_length constraints.
    """
    user = User(email="title_constraint_user@example.com", password_hash="title_hash")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    user_id = user.id

    # Test max length (100 chars)
    long_title = "A" * 101 # Max length is 100, so 101 should fail
    todo_long_title = Todo(user_id=user_id, title=long_title)
    db_session.add(todo_long_title)
    with pytest.raises(Exception) as excinfo_max: # Expecting a constraint violation error
        db_session.commit()
    db_session.rollback() # Rollback to clear the failed transaction
    assert "value too long" in str(excinfo_max.value).lower() or "max_length" in str(excinfo.value).lower()
    print("Todo title max length constraint enforced successfully.")

    # Test min length (1 char)
    empty_title = ""
    todo_empty_title = Todo(user_id=user_id, title=empty_title)
    db_session.add(todo_empty_title)
    with pytest.raises(Exception) as excinfo_min: # Expecting a constraint violation error
        db_session.commit()
    db_session.rollback() # Rollback to clear the failed transaction
    assert "length must be at least 1" in str(excinfo_min.value).lower() or "min_length" in str(excinfo.value).lower()
    print("Todo title min length constraint enforced successfully.")

def test_todo_description_max_length_constraint(db_session: Session):
    """
    Test that the description field adheres to its maximum length constraint.
    """
    user = User(email="desc_maxlength_user@example.com", password_hash="desc_hash")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    user_id = user.id

    long_description = "B" * 501 # Max length is 500, so 501 should fail
    todo_long_desc = Todo(user_id=user_id, title="Task with long description", description=long_description)
    db_session.add(todo_long_desc)
    
    with pytest.raises(Exception) as excinfo: # Expecting a constraint violation error
        db_session.commit()
        
    db_session.rollback() # Rollback to clear the failed transaction

    assert "value too long" in str(excinfo.value).lower() or "max_length" in str(excinfo.value).lower()
    print("Todo description max length constraint enforced successfully.")

def test_todo_completed_default_value(db_session: Session):
    """
    Test that the 'completed' field defaults to False if not specified.
    """
    user = User(email="default_completed_user@example.com", password_hash="default_hash")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    user_id = user.id

    todo_without_completed = Todo(user_id=user_id, title="Task with default completed")
    db_session.add(todo_without_completed)
    db_session.commit()
    db_session.refresh(todo_without_completed)

    assert todo_without_completed.completed is False
    print("Todo 'completed' field defaults to False successfully.")