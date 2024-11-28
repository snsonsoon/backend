from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Users(SQLModel, table=True):
    user_id: str = Field(primary_key=True, unique=True, max_length=50)
    password: str = Field(nullable=False, max_length=255)
    nickname: str = Field(nullable=False, max_length=50)

    # Relationships
    reviews: List["Reviews"] = Relationship(back_populates="users")
