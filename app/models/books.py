from sqlmodel import SQLModel, Field, Relationship

class Books(SQLModel, table=True):
    isbn: str = Field(primary_key=True, max_length=13)
    book_title: str = Field(nullable=False, max_length=255)
    author: str = Field(nullable=False, max_length=255)
    publisher: str = Field(nullable=False, max_length=255)
    publication_year: int = Field(nullable=False)
    genre: str | None = Field(default=None, max_length=50)
    cover_image: str | None = Field(default=None, max_length=255)

    # Relationships
    reviews: list["Reviews"] = Relationship(back_populates="books")
    booklibraries: list["BookLibraries"] = Relationship(back_populates="books")