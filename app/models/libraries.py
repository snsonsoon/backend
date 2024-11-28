from sqlmodel import SQLModel, Field, Relationship

class Libraries(SQLModel, table=True):
    library_id: int = Field(primary_key=True)
    library_name: str = Field(nullable=False, max_length=255)
    address: str = Field(nullable=False, max_length=255)
    homepage: str | None = Field(default=None, max_length=255)

    booklibraries: list["BookLibraries"] = Relationship(back_populates="libraries")