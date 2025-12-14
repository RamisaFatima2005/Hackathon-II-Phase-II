from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from .user import User


class Todo(SQLModel, table=True):
    """
    Represents a todo item in the Full-Stack Todo Application.

    Attributes:
        id (Optional[int]): The unique identifier for the todo item.
                            Automatically generated if not provided.
        user_id (int): The ID of the user who owns this todo item.
                       Foreign key to the User table, and indexed for efficient lookups.
        title (str): A brief title for the todo item.
                     Must be between 1 and 100 characters.
        description (Optional[str]): A more detailed description for the todo item.
                                     Optional, with a maximum length of 500 characters.
        completed (bool): A flag indicating whether the todo item is completed.
                          Defaults to False.
        created_at (datetime): The timestamp when the todo item was created.
                               Defaults to the current UTC time.

        user (Optional[User]): The User object related to this todo item.
                               This is a relationship field, not stored directly in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=100, min_length=1)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Define the relationship to the User model
    user: Optional[User] = Relationship(back_populates="todos")

    def __repr__(self) -> str:
        return f"Todo(id={self.id}, title='{self.title}', user_id={self.user_id}, completed={self.completed})"

    class Config:
        from_attributes = True
