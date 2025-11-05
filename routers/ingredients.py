from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime

from core.database import SessionLocal
from models.ingredient import Ingredient
from schemas.ingredient import Ingredient as IngredientSchema, IngredientCreate, IngredientUpdate
from routers.auth import get_current_user, get_db
from models.user import User

router = APIRouter()

@router.post("/", response_model=IngredientSchema, status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    ingredient: IngredientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Ingredient).execution_options(include_deleted=True).where(Ingredient.name == ingredient.name)
    )
    db_ingredient = result.scalars().first()
    if db_ingredient:
        raise HTTPException(status_code=400, detail="Ingredient with this name already exists")

    new_ingredient = Ingredient(
        name=ingredient.name,
        category=ingredient.category
    )
    db.add(new_ingredient)
    await db.commit()
    await db.refresh(new_ingredient)
    return new_ingredient

@router.get("/", response_model=List[IngredientSchema])
async def read_ingredients(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ingredient))
    ingredients = result.scalars().all()
    return ingredients

@router.get("/{ingredient_id}", response_model=IngredientSchema)
async def read_ingredient(ingredient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ingredient).where(Ingredient.id == ingredient_id))
    ingredient = result.scalars().first()
    if ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    return ingredient

@router.put("/{ingredient_id}", response_model=IngredientSchema)
async def update_ingredient(
    ingredient_id: int,
    ingredient_update: IngredientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Ingredient).where(Ingredient.id == ingredient_id))
    ingredient = result.scalars().first()

    if ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    
    ingredient_data = ingredient_update.dict(exclude_unset=True)
    for key, value in ingredient_data.items():
        setattr(ingredient, key, value)
    
    db.add(ingredient)
    await db.commit()
    await db.refresh(ingredient)
    return ingredient

@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingredient(
    ingredient_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Ingredient).where(Ingredient.id == ingredient_id))
    ingredient = result.scalars().first()

    if ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    
    ingredient.deleted_at = datetime.utcnow()
    db.add(ingredient)
    await db.commit()
    return {"message": "Ingredient deleted successfully"}
