from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class BookLibraries(SQLModel, table=True):
    isbn: str = Field(primary_key=True, max_length=13, foreign_key="books.isbn")
    library_id: int = Field(primary_key=True, foreign_key="libraries.library_id")
    availability: bool = Field(default=True)

    # Relationships
    books: "Books" = Relationship(back_populates="booklibraries")
    libraries: "Libraries" = Relationship(back_populates="booklibraries")
