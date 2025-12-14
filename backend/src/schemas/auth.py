from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any

class SignupRequest(BaseModel):
    """
    Request schema for user signup.
    """
    email: EmailStr = Field(index=True, description="User's unique email address")
    password: str = Field(min_length=8, max_length=100, description="User's password")

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
            }
        }

class SigninRequest(BaseModel):
    """
    Request schema for user signin.
    """
    email: EmailStr = Field(index=True, description="User's registered email address")
    password: str = Field(description="User's password")

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
            }
        }

class AuthResponse(BaseModel):
    """
    Response schema for successful authentication (signup/signin).
    Includes access token and user details.
    """
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    message: str = "Authentication successful"

    class Config:
        from_attributes = True # Allows base model to be created from ORM models

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class ErrorResponse(BaseModel):
    """
    Standard response schema for API errors.
    """
    error: str
    code: int
    details: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Internal Server Error",
                "code": 500,
                "details": {"reason": "Something went wrong"},
            }
        }