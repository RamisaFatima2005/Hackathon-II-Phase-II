# test_auth_api.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from jose import JWTError # Import JWTError for exception handling

# Assuming main app and models/schemas are in the correct structure
# Need to ensure correct imports relative to the project root
# If main.py is in backend/src/, then 'from backend.src.main import app' is correct.
from backend.src.main import app 
from backend.src.database import get_session, engine, create_db_and_tables # Import DB setup
from backend.src.models.user import User
from backend.src.dependencies import get_current_user # Will be used by other endpoints, not directly tested here
from backend.src.services.auth_utils import get_password_hash
from backend.src.services.jwt_handler import create_access_token
from backend.src.schemas.auth import SignupRequestSchema, SigninRequestSchema, AuthResponse # For request/response bodies

# --- Test Setup ---
# Use an in-memory SQLite database for tests
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}, # Needed for SQLite
    poolclass=StaticPool,
)

def override_get_session():
    """Overrides the get_session dependency to use the test engine."""
    SQLModel.metadata.create_all(engine) # Create tables for the test DB
    with Session(engine) as session:
        yield session

# Override the global dependency for get_session
app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)

# --- Test Constants ---
TEST_EMAIL_1 = "testuser1@example.com"
TEST_PASSWORD_1 = "password123"
TEST_EMAIL_2 = "testuser2@example.com"
TEST_PASSWORD_2 = "securepassword456"

# --- Test Functions ---

def test_signup_success():
    """Tests successful user registration."""
    response = client.post("/auth/signup", json={
        "email": TEST_EMAIL_1,
        "password": TEST_PASSWORD_1
    })
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["email"] == TEST_EMAIL_1
    assert data["message"] == "User created and logged in successfully."
    # Optionally, check if user is created in DB (requires access to test_engine or session)

def test_signup_duplicate_email():
    """Tests signup with an email that is already registered."""
    # First, register the user successfully
    client.post("/auth/signup", json={
        "email": TEST_EMAIL_1,
        "password": TEST_PASSWORD_1
    })
    
    # Attempt to register again with the same email
    response = client.post("/auth/signup", json={
        "email": TEST_EMAIL_1,
        "password": "anotherpassword"
    })
    assert response.status_code == 409 # Conflict
    assert response.json()["detail"] == "Email already registered."

def test_signin_success():
    """Tests successful user login."""
    # First, register a user to test signin
    client.post("/auth/signup", json={
        "email": TEST_EMAIL_1,
        "password": TEST_PASSWORD_1
    })

    response = client.post("/auth/signin", json={
        "email": TEST_EMAIL_1,
        "password": TEST_PASSWORD_1
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["email"] == TEST_EMAIL_1
    assert data["message"] == "Login successful."

    # Verify the token can be used to get current user (this implicitly tests the dependency)
    # We need a protected endpoint to test this. For now, we assume get_current_user works if signin is successful.
    # A more thorough test would involve calling an actual protected endpoint.
    # For simplicity, we'll consider the successful token generation as partial verification.
    # Example: user_response = client.get("/some-protected-endpoint", headers={"Authorization": f"Bearer {data['access_token']}"})
    # assert user_response.status_code == 200 # Or expected success code

def test_signin_wrong_password():
    """Tests login with an incorrect password."""
    client.post("/auth/signup", json={
        "email": TEST_EMAIL_1,
        "password": TEST_PASSWORD_1
    })

    response = client.post("/auth/signin", json={
        "email": TEST_EMAIL_1,
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password."

def test_signin_nonexistent_email():
    """Tests login with an email that is not registered."""
    response = client.post("/auth/signin", json={
        "email": "nonexistent@example.com",
        "password": "anypassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password."

# --- Note on Test Coverage ---
# This test suite covers basic signup and signin functionality.
# Further tests should include:
# - Password complexity requirements (if any are enforced server-side)
# - Token expiration and refresh logic (if implemented)
# - Role-based access control (if applicable)
# - More edge cases for invalid inputs and error handling.
