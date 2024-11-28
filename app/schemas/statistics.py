from pydantic import BaseModel

class UserStatisticsResponse(BaseModel):
    user_id: str
    average_rating: float
    total_reviews: int
    percentile: float | None = None  # Optional if percentile isn't always needed
