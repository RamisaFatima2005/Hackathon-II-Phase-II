# auth.py (updated with signin endpoint)
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.concurrency import run_in_threadpool
from sqlmodel import Session, select

from ..database import get_session # Assuming get_session is correctly imported
from ..models.user import User
from ..services.auth_utils import get_password_hash, verify_password # Import verify_password for signin
from ..services.jwt_handler import create_access_token # Import for token generation
from ..dependencies import get_authenticated_user_id, get_current_active_user # For authentication dependencies
from ..schemas.auth import TokenSchema, SignupRequest, SigninRequest, AuthResponse # Explicitly import schemas

import logging # Import the logging module

# --- Logger Configuration ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # Set the root logger level

# --- FastAPI Router Definition ---
router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- Helper function to format User model for API response ---
def format_user_response(user: User) -> Dict[str, Any]:
    """Formats a User object into a dictionary suitable for API response."""
    return {
        "id": user.id,
        "email": user.email,
        # Assuming created_at is a datetime object, format it to ISO string
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }

# --- Authentication Endpoints ---

@router.post("/signup", response_model=AuthResponse)
async def signup(
    user_data: SignupRequest, # Use the imported schema for request body
    session: Session = Depends(get_session)
):
    """
    Registers a new user or logs in an existing user if email already registered.
    Expects email and password in the request body.
    """
    logger.info(f"Attempting signup for email: {user_data.email}")
    
    # Check if user already exists
    existing_user = await run_in_threadpool(
        lambda: session.exec(select(User).where(User.email == user_data.email)).first()
    )
    
    if existing_user:
        logger.info(f"Email {user_data.email} already registered. Attempting to sign in.")
        # If user exists, try to sign them in
        if not verify_password(user_data.password, existing_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered, incorrect password.",
            )
        
        # If password is correct, generate token and return AuthResponse
        access_token = create_access_token(subject=str(existing_user.id))
        response_data = AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=existing_user.id,
            email=existing_user.email,
            message="Logged in successfully."
        )
        return response_data

    try:
        # Hash the password
        hashed_password = get_password_hash(user_data.password)
        
        # Create new user instance
        new_user = User(
            email=user_data.email, 
            password_hash=hashed_password, 
            created_at=datetime.now(timezone.utc)
        )
        
        await run_in_threadpool(session.add, new_user)
        await run_in_threadpool(session.commit)
        await run_in_threadpool(session.refresh, new_user)
        
        # Create JWT token for the new user
        access_token = create_access_token(subject=str(new_user.id))
        
        logger.info(f"User registered successfully: {new_user.email} (ID: {new_user.id})")

        # Prepare response including token and basic user info
        response_data = AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=new_user.id,
            email=new_user.email,
            message="User created and logged in successfully."
        )
        
        return response_data

    except HTTPException as e:
        logger.error(f"HTTP Exception during signup for {user_data.email}: {e.detail}")
        raise e # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Unexpected error during signup for {user_data.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during signup. Please try again later."
        )

@router.post("/signin", response_model=AuthResponse)
async def signin(
    user_data: SigninRequest, # Use the imported schema for request body
    session: Session = Depends(get_session)
):
    """
    Authenticates a user and returns a JWT access token.
    Expects email and password in the request body.
    """
    logger.info(f"Attempting signin for email: {user_data.email}")
    
    try:
        # Fetch user by email
        user = session.exec(select(User).where(User.email == user_data.email)).first()
        
        # Check if user exists and if the password is correct
        if not user or not verify_password(user_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create JWT token
        access_token = create_access_token(subject=str(user.id))
        
        logger.info(f"User signed in successfully: {user.email} (ID: {user.id})")

        # Prepare response including token and basic user info
        response_data = AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            email=user.email,
            message="Login successful."
        )
        
        return response_data

    except HTTPException as e:
        logger.error(f"HTTP Exception during signin for {user_data.email}: {e.detail}")
        raise e # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Unexpected error during signin for {user_data.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login. Please try again later."
        )

# --- Get Current User Endpoint ---

@router.get("/current_user", response_model=Dict[str, Any])
async def get_current_user_endpoint(current_user: User = Depends(get_current_active_user)):
    """
    Get the current authenticated user's information.
    """
    logger.info(f"Fetching current user: {current_user.email} (ID: {current_user.id})")
    return format_user_response(current_user)


