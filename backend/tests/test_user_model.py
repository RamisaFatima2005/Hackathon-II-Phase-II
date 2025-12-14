import pytest
from sqlmodel import Session

# Assuming backend/src/models/user.py and backend/src/models/__init__.py are available
# and that models are imported correctly in backend/src/models/__init__.py
# Ensure the following imports work in your test environment.
# If running tests from the root, imports might look like:
# from backend.src.models import User
# from backend.src.models.user import User # if __init__.py doesn't re-export
# For simplicity, assuming direct import from models.user is possible
try:
    from backend.src.models.user import User
    from backend.src.models import User # For type hinting if needed for Session context
except ImportError:
    pytest.skip("Could not import User model. Ensure backend.src.models is in PYTHONPATH.", allow_module_level=True)


# --- Test Setup ---
# We reuse the 'engine' and 'db_session' fixtures from test_database_connection.py
# assuming they are discoverable by pytest and correctly configured.
# If these fixtures were in a separate conftest.py, they would be auto-detected.
# For this standalone file, we'll assume they are available or defined elsewhere.

# If test_database_connection.py is in the same directory and pytest is run from backend/tests/
# then fixtures from that file should be available.
# If not, you might need to explicitly import them or use a conftest.py

# --- Test Cases for User Model CRUD ---

def test_create_user(db_session: Session):
    """
    Test creating a new user and adding it to the database.
    Verifies that basic user creation and saving works.
    """
    user = User(email="testuser@example.com", password_hash="hashed_password")
    db_session.add(user)
    db_session.commit()
    
    db_session.refresh(user) # Refresh to get the assigned ID and other database defaults

    assert user.id is not None
    assert user.email == "testuser@example.com"
    assert user.password_hash == "hashed_password"
    assert user.created_at is not None
    print(f"User created: {user}")

def test_read_user(db_session: Session):
    """
    Test retrieving a user from the database by email.
    Verifies that users can be queried.
    """
    # First, create a user to read
    user_to_create = User(email="readuser@example.com", password_hash="read_hash")
    db_session.add(user_to_create)
    db_session.commit()
    db_session.refresh(user_to_create)
    
    # Read the user back
    retrieved_user = db_session.query(User).filter(User.email == "readuser@example.com").first()
    
    assert retrieved_user is not None
    assert retrieved_user.id == user_to_create.id
    assert retrieved_user.email == "readuser@example.com"
    assert retrieved_user.password_hash == "read_hash"
    print(f"User retrieved: {retrieved_user}")

def test_update_user(db_session: Session):
    """
    Test updating an existing user's details.
    Verifies that changes are committed to the database.
    """
    # Create a user to update
    user_to_update = User(email="updateuser@example.com", password_hash="old_hash")
    db_session.add(user_to_update)
    db_session.commit()
    db_session.refresh(user_to_update)
    
    # Update the user's password hash
    new_password_hash = "new_hashed_password"
    user_to_update.password_hash = new_password_hash
    db_session.add(user_to_update)
    db_session.commit()
    
    # Refresh to ensure changes are loaded from DB
    db_session.refresh(user_to_update)
    
    assert user_to_update.password_hash == new_password_hash
    print(f"User updated. New hash: {user_to_update.password_hash}")

def test_delete_user(db_session: Session):
    """
    Test deleting a user from the database.
    Verifies that the user is removed.
    """
    # Create a user to delete
    user_to_delete = User(email="deleteuser@example.com", password_hash="delete_hash")
    db_session.add(user_to_delete)
    db_session.commit()
    db_session.refresh(user_to_delete)
    
    user_id_to_delete = user_to_delete.id
    
    # Delete the user
    user = db_session.query(User).filter(User.id == user_id_to_delete).first()
    if user:
        db_session.delete(user)
        db_session.commit()
        
        # Verify deletion
        deleted_user = db_session.query(User).filter(User.id == user_id_to_delete).first()
        assert deleted_user is None
        print(f"User with ID {user_id_to_delete} deleted successfully.")
    else:
        pytest.fail("User to delete not found.")

def test_unique_email_constraint(db_session: Session):
    """
    Test that the unique constraint on email is enforced.
    Creating a second user with the same email should raise an integrity error.
    """
    # Create the first user
    user1 = User(email="unique@example.com", password_hash="hash1")
    db_session.add(user1)
    db_session.commit()
    db_session.refresh(user1)
    
    # Attempt to create a second user with the same email
    user2 = User(email="unique@example.com", password_hash="hash2")
    db_session.add(user2)
    
    # Committing should raise an IntegrityError due to the unique constraint
    with pytest.raises(Exception) as excinfo: # Catching generic Exception as specific DB error might vary
        db_session.commit()
        
    # Rollback to clear the failed transaction and allow next tests to run
    db_session.rollback()
    
    assert "unique constraint" in str(excinfo.value).lower() or "duplicate key value" in str(excinfo.value).lower()
    print("Unique email constraint enforced successfully.")

