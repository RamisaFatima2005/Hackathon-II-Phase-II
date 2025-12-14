from datetime import datetime
import logging # Import the logging module
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, Depends, HTTPException, status, Path
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, create_engine, select, SQLModel

from .database import get_session, engine, create_db_and_tables # Assuming these are defined
from .models.user import User # For user model import
from .models.todo import Todo # For todo model import
from .services.auth_utils import get_password_hash, verify_password # For auth utilities
from .services.jwt_handler import create_access_token # For JWT token generation
from .dependencies import get_authenticated_user_id # For authentication dependency

# Import routers
from .api.auth import router as auth_router
# Import tasks router from its module
from .api.tasks import router as tasks_router

import uvicorn # For running the development server

# --- Basic Logging Configuration ---
# Configure logging for the application
# NFR-007: Logging - Configure logging for the application to capture requests, errors, and important events.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # Set the root logger level

# --- FastAPI Application Instance ---
app = FastAPI(
    title="Todo API - Hackathon Phase 2",
    description="Multi-user task management with JWT auth",
    version="1.0.0",
)

# --- CORS Configuration ---
# Allowing all origins for development purposes. In production, restrict this to specific domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production: ["http://localhost:3000", "your_vercel_domain"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Startup Event ---
@app.on_event("startup")
async def startup_event():
    """
    Startup event handler for the FastAPI application.
    This function is called once when the application starts.
    It's a good place to perform one-time setup tasks.
    """
    logger.info("Application starting up...") # Use logger for startup message
    try:
        # Initialize database tables if they don't exist
        # This function comes from backend.src.database
        create_db_and_tables()
        logger.info("Database tables ensured.") # Use logger for info messages
    except Exception as e:
        logger.error(f"Error during database initialization: {e}") # Use logger for errors
        # In a real application, you might want to log this error or handle it more gracefully.
        # For now, we'll let the application continue, but this is a critical failure point if DB is needed.

# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root() -> Dict[str, str]:
    """
    Root endpoint for the API.
    Provides basic API information.
    """
    logger.debug("Root endpoint accessed.") # Example of debug logging
    return {
        "message": "Welcome to the Todo API!",
        "version": app.version,
        "docs": "/docs"
    }

# --- Include Routers ---
# Include authentication routes
app.include_router(auth_router)

# Include tasks router
app.include_router(tasks_router, prefix="/api/{user_id}") # Include tasks router with prefix


# --- Main Execution Block ---
# This block allows running the application directly using `python -m backend.src.main`
# It's typically used for development servers.
if __name__ == "__main__":
    # Note: For production deployment (e.g., Vercel), you typically don't run uvicorn directly.
    # Vercel or other deployment platforms handle the ASGI application startup.
    logger.info("Running FastAPI application with uvicorn...") # Use logger
    uvicorn.run(
        "backend.src.main:app", # Module path to the FastAPI app instance
        host="0.0.0.0", 
        port=8000, 
        reload=True # Enable auto-reloading for development
    )