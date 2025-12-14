from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    """
    Represents a user in the Full-Stack Todo Application.

    Attributes:
        id (Optional[int]): The unique identifier for the user.
                            Automatically generated if not provided.
        email (str): The unique email address of the user, used for login.
                     Must be unique and is indexed for faster lookups.
        password_hash (str): The hashed password of the user.
                             Stored securely using bcrypt.
        created_at (datetime): The timestamp when the user account was created.
                               Defaults to the current UTC time.

        todos (List["Todo"]): A list of Todo items owned by this user.
                              This is a relationship field, not stored directly in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    todos: List["Todo"] = Relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<{type(self).__name__} at {hex(id(self))}>"

    class Config:
        # Enable ORM mode for SQLModel
        from_attributes = True
