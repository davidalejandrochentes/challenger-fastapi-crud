from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional
from .user import User
from .review import Review
from .recipe_ingredient import RecipeIngredient, RecipeIngredientCreate

class DifficultyEnum(str, Enum):
    easy = 'easy'
    medium = 'medium'
    hard = 'hard'

class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: Optional[int] = None
    difficulty: Optional[DifficultyEnum] = None

class RecipeCreate(RecipeBase):
    ingredients: List[RecipeIngredientCreate] = Field(
        default_factory=list,
        example=[
            {"ingredient_id": 1, "quantity": "100", "unit": "g"},
            {"ingredient_id": 2, "quantity": "1", "unit": "unidad"}
        ]
    )

class RecipeUpdate(RecipeBase):
    title: Optional[str] = None
    ingredients: Optional[List[RecipeIngredientCreate]] = None

class Recipe(RecipeBase):
    id: int
    user_id: int
    user: User
    reviews: List[Review] = []
    ingredients: List[RecipeIngredient] = []

    class Config:
        from_attributes = True
