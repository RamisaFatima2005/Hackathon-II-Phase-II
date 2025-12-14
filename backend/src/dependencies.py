
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer # For extracting token from header
from sqlmodel import Session, select

from .database import get_session # Assuming get_session is correctly imported
from .models.user import User
from .services.auth_utils import get_password_hash, verify_password # Import hashing utilities
from .services.jwt_handler import create_access_token, verify_access_token # Import JWT functions
from .schemas.auth import TokenSchema, SignupRequest, SigninRequest, AuthResponse # Explicitly import schemas

import logging # Import the logging module

# --- Logger Configuration ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # Set the root logger level

# --- Security Settings for JWT ---
# These should ideally be loaded from environment variables in a real application.
# For development/testing purposes, placeholder values are used here.
# NEVER hardcode secrets in production code.
SECRET_KEY = "CX3IOcFJFW5xzhSTZbpVyQrzOVnsQEw3wzhd2s-T0CqFi9iKve7BWxXzJCVC4OHlvp8"  # CHANGE THIS IN PRODUCTION!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token expires in 30 minutes

# --- OAuth2 Scheme for Bearer Token ---
# This will look for a token in the Authorization header in the format "Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

# --- Dependency to get current user ID ---
async def get_authenticated_user_id(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> int:
    """
    Dependency to get the ID of the current authenticated user.
    Verifies the JWT token and extracts the user ID from it.
    Raises HTTPException if the token is invalid or user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        user_id_str = verify_access_token(token=token)
        if user_id_str is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user_id = int(user_id_str)
    # Ensure the user actually exists in the database
    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception
        
    return user_id

# --- Dependency to get current active user object ---
async def get_current_active_user(
    user_id: int = Depends(get_authenticated_user_id),
    session: Session = Depends(get_session)
) -> User:
    """
    Dependency to get the current authenticated user object.
    Fetches the user object from the database using the authenticated user ID.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

