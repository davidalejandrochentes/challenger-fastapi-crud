from pydantic import BaseModel
from typing import Optional
from .ingredient import Ingredient

class RecipeIngredientBase(BaseModel):
    ingredient_id: int
    quantity: str
    unit: Optional[str] = None

class RecipeIngredientCreate(RecipeIngredientBase):
    pass

class RecipeIngredientUpdate(RecipeIngredientBase):
    pass

class RecipeIngredient(RecipeIngredientBase):
    id: int
    recipe_id: int
    ingredient: Optional[Ingredient] = None

    class Config:
        from_attributes = True
