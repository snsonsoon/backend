from sqlmodel import SQLModel, Field
from typing import Optional

class BookStatistics(SQLModel, table=True): 
    isbn: str = Field(primary_key=True, max_length=13)
    average_rating: Optional[float] = Field(default=0)
    total_reviews: Optional[int] = Field(default=0)

class UserStatistics(SQLModel, table=True):
    user_id: str = Field(primary_key=True, max_length=50)
    average_rating: Optional[float] = Field(default=0)
    total_reviews: Optional[int] = Field(default=0)

class UserReviewGenres(SQLModel, table=True): 
    user_id: str = Field(primary_key=True, max_length=50)
    genre: str = Field(primary_key=True, max_length=50)
    review_count: Optional[int] = Field(default=0)
