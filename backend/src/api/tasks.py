import logging
import traceback
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlmodel import Session, select
from pydantic import BaseModel, Field # Added this import

from ..database import get_session, engine, create_db_and_tables
from ..models.user import User
from ..models.todo import Todo
from ..dependencies import get_authenticated_user_id
from ..schemas.auth import TokenSchema # Assuming TokenSchema is available
from ..schemas.tasks import TaskCreateSchema, TaskUpdateSchema # Assuming Task schemas are in schemas.tasks

# Import routers
# Assuming auth router is already set up and imported in main.py
# from backend.src.api.auth import router as auth_router 

# --- Logger Configuration ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # Set the logger level

# Define the router for tasks
router = APIRouter(tags=["Tasks"])

# --- Helper function to format Todo model for API response ---
def format_todo_response(todo: Todo) -> Dict[str, Any]:
    """Formats a Todo object into a dictionary suitable for API response."""
    return {
        "id": todo.id,
        "user_id": todo.user_id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "created_at": todo.created_at.isoformat() if todo.created_at else None,
    }

# --- API Endpoints for Tasks ---

@router.get("/tasks", response_model=List[Dict[str, Any]])
async def get_all_tasks(
    user_id: int = Path(..., description="ID of the user to retrieve tasks for. Must match authenticated user's ID."),
    current_user_id: int = Depends(get_authenticated_user_id),
    session: Session = Depends(get_session)
) -> List[Dict[str, Any]]:
    """
    Retrieves all tasks for a specific user.
    Requires JWT authentication and verifies user_id matches authenticated user.
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other user's tasks."
        )
    
    try:
        statement = select(Todo).where(Todo.user_id == user_id).order_by(Todo.created_at.desc())
        tasks = session.exec(statement).all()
        
        formatted_tasks = [format_todo_response(task) for task in tasks]
        
        return formatted_tasks
    except Exception as e:
        logger.error(f"Error fetching tasks for user {user_id}: {e}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks."
        )

@router.post("/tasks", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreateSchema, # Using the imported schema
    current_user_id: int = Depends(get_authenticated_user_id),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    Creates a new todo task for the authenticated user.
    """
    logger.info(f"Attempting to create task for user {current_user_id} with data: {task_data.model_dump()}")
    try:
        new_task = Todo(
            user_id=current_user_id,
            title=task_data.title,
            description=task_data.description,
            completed=False,
            created_at=datetime.now(timezone.utc)
        )
        logger.info(f"New task object created: {new_task}")
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        
        formatted_task = format_todo_response(new_task)
        logger.info(f"Task created successfully: {new_task.id} for user {current_user_id}")
        
        return {"data": formatted_task, "message": "Task created successfully."}
    except Exception as e:
        logger.error(f"Error creating task for user {current_user_id}: {e}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task."
        )

@router.get("/tasks/{id}", response_model=Dict[str, Any])
async def get_task_by_id(
    user_id: int = Path(..., description="ID of the user who owns the task. Must match authenticated user's ID."),
    id: int = Path(..., description="ID of the task to retrieve."),
    current_user_id: int = Depends(get_authenticated_user_id),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    Retrieves a single task by ID for a specific user.
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other user's tasks."
        )
        
    try:
        statement = select(Todo).where(Todo.id == id, Todo.user_id == user_id)
        task = session.exec(statement).first()
        
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found for user {user_id}.")
            
        formatted_task = format_todo_response(task)
        
        return {"data": formatted_task, "message": "Task retrieved successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching task {id} for user {user_id}: {e}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task."
        )

@router.put("/tasks/{id}", response_model=Dict[str, Any])
async def update_task(
    task_data: TaskUpdateSchema, # Using TaskUpdateSchema
    user_id: int = Path(..., description="ID of the user who owns the task. Must match authenticated user's ID."),
    id: int = Path(..., description="ID of the task to update."),
    current_user_id: int = Depends(get_authenticated_user_id),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    Updates an existing task by ID for a specific user.
    Allows partial updates if fields are provided in the request.
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update tasks belonging to other users."
        )
        
    try:
        task = session.get(Todo, id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found.")
        
        if task.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Task does not belong to the authenticated user."
            )

        # Update fields if they are provided in the request body
        update_data = task_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
            
        session.add(task)
        session.commit()
        session.refresh(task)
        
        formatted_task = format_todo_response(task)

        return {"data": formatted_task, "message": "Task updated successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error updating task {id} for user {current_user_id}: {e}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task."
        )

@router.patch("/tasks/{id}/complete", response_model=Dict[str, Any])
async def toggle_task_completion(
    user_id: int = Path(..., description="ID of the user who owns the task. Must match authenticated user's ID."),
    id: int = Path(..., description="ID of the task to toggle completion status."),
    current_user_id: int = Depends(get_authenticated_user_id),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    Toggles the completion status of a task by ID for a specific user.
    Expects a payload like {"completed": true/false}.
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot toggle completion status for tasks belonging to other users."
        )
        
    try:
        task = session.get(Todo, id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found.")
        
        if task.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Task does not belong to the authenticated user."
            )

        # Toggle the completion status
        task.completed = not task.completed
        
        session.add(task)
        session.commit()
        session.refresh(task)
        
        message = f"Task '{task.title}' marked as {'completed' if task.completed else 'incomplete'}."
        
        formatted_task = format_todo_response(task)

        return {"data": formatted_task, "message": message}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error toggling completion for task {id} for user {current_user_id}: {e}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to toggle task completion status."
        )

@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: int = Path(..., description="ID of the user who owns the task. Must match authenticated user's ID."),
    id: int = Path(..., description="ID of the task to delete."),
    current_user_id: int = Depends(get_authenticated_user_id),
    session: Session = Depends(get_session)
) -> None:
    """
    Deletes a task by ID for a specific user.
    Returns 204 No Content on successful deletion.
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete tasks belonging to other users."
        )
        
    try:
        task = session.get(Todo, id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} not found.")
        
        if task.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Task does not belong to the authenticated user."
            )

        session.delete(task)
        session.commit()
        
        # No content to return on successful deletion (204)
        return None 
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting task {id} for user {current_user_id}: {e}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task."
        )
