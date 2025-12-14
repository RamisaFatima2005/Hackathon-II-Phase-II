from pydantic import BaseModel, Field
from typing import Optional

class TaskCreateSchema(BaseModel):
    """
    Schema for creating a new task.
    """
    title: str = Field(min_length=1, max_length=100, description="The title of the task.")
    description: Optional[str] = Field(default=None, max_length=500, description="Optional detailed description of the task.")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, cheese",
            }
        }

class TaskUpdateSchema(BaseModel):
    """
    Schema for updating an existing task. Allows partial updates.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=100, description="The updated title of the task.")
    description: Optional[str] = Field(default=None, max_length=500, description="The updated description of the task.")
    completed: Optional[bool] = Field(default=None, description="The updated completion status of the task.")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Grocery List",
                "description": "Milk, eggs, bread, cheese, and juice",
                "completed": True,
            }
        }