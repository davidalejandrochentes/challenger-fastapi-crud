from pydantic import BaseModel, constr
from typing import Optional
from .user import User

class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    recipe_id: int

class ReviewUpdate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    user_id: int
    recipe_id: int
    user: User

    class Config:
        from_attributes = True
