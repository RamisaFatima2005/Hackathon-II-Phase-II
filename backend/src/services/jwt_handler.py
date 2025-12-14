# jwt_handler.py
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
# Removed passlib imports as they are for password hashing, not JWT.
# from passlib.context import CryptContext # Using passlib for context
# from passlib.bcrypt import BcryptContext # Specific implementation for bcrypt

# --- Security Settings ---
# IMPORTANT: These should be loaded from environment variables in a real application.
# For development/testing purposes, placeholder values are used here.
# NEVER hardcode secrets in production code.
SECRET_KEY = "your-super-secret-key-change-me" # CHANGE THIS IN PRODUCTION!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token expires in 30 minutes

# --- JWT Token Generation and Verification ---

def create_access_token(subject: str, expires_delta: timedelta = None) -> str:
    """
    Creates a JWT access token.
    `subject` is typically the user ID or email.
    `expires_delta` is an optional timedelta for token expiration.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> Optional[str]:
    """
    Verifies a JWT access token and returns the subject (e.g., user ID).
    Returns None if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject = payload.get("sub")
        if subject is None:
            return None
        return subject
    except JWTError:
        return None