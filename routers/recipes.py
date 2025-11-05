from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime

from core.database import SessionLocal
from models.recipe import Recipe
from models.recipe_ingredient import RecipeIngredient
from schemas.recipe import Recipe as RecipeSchema, RecipeCreate, RecipeUpdate, DifficultyEnum
from schemas.recipe_ingredient import RecipeIngredientCreate
from routers.auth import get_current_user, get_db
from models.user import User

router = APIRouter()

@router.post("/", response_model=RecipeSchema, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe: RecipeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        instructions=recipe.instructions,
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        servings=recipe.servings,
        difficulty=recipe.difficulty.value if recipe.difficulty else None,
        user_id=current_user.id
    )
    db.add(new_recipe)
    await db.flush()

    recipe_id = new_recipe.id

    for ingredient_data in recipe.ingredients:
        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe_id,
            ingredient_id=ingredient_data.ingredient_id,
            quantity=ingredient_data.quantity,
            unit=ingredient_data.unit
        )
        db.add(recipe_ingredient)
    
    await db.commit()
    
    result = await db.execute(
        select(Recipe)
        .options(
            selectinload(Recipe.user),
            selectinload(Recipe.reviews),
            selectinload(Recipe.ingredients).selectinload(RecipeIngredient.ingredient)
        )
        .where(Recipe.id == recipe_id)
    )
    final_recipe = result.scalars().first()
    return final_recipe

@router.get("/", response_model=List[RecipeSchema])
async def read_recipes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Recipe).options(
            selectinload(Recipe.user),
            selectinload(Recipe.reviews),
            selectinload(Recipe.ingredients).selectinload(RecipeIngredient.ingredient)
        )
    )
    recipes = result.scalars().all()
    return [recipe for recipe in recipes if recipe.user is not None]

@router.get("/{recipe_id}", response_model=RecipeSchema)
async def read_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Recipe)
        .options(
            selectinload(Recipe.user),
            selectinload(Recipe.reviews),
            selectinload(Recipe.ingredients).selectinload(RecipeIngredient.ingredient)
        )
        .where(Recipe.id == recipe_id)
    )
    recipe = result.scalars().first()
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe

@router.put("/{recipe_id}", response_model=RecipeSchema)
async def update_recipe(
    recipe_id: int,
    recipe_update: RecipeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Recipe)
        .options(selectinload(Recipe.ingredients))
        .where(Recipe.id == recipe_id)
    )
    recipe = result.scalars().first()

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    
    if recipe.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this recipe")
    
    recipe_data = recipe_update.dict(exclude_unset=True)
    for key, value in recipe_data.items():
        if key == "difficulty" and value is not None:
            setattr(recipe, key, value.value)
        elif key != "ingredients":
            setattr(recipe, key, value)
    
    if recipe_update.ingredients is not None:
        for rec_ing in recipe.ingredients:
            await db.delete(rec_ing)
        await db.flush()

        for ingredient_data in recipe_update.ingredients:
            recipe_ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient_data.ingredient_id,
                quantity=ingredient_data.quantity,
                unit=ingredient_data.unit
            )
            db.add(recipe_ingredient)

    await db.commit()

    result = await db.execute(
        select(Recipe)
        .options(
            selectinload(Recipe.user),
            selectinload(Recipe.reviews),
            selectinload(Recipe.ingredients).selectinload(RecipeIngredient.ingredient)
        )
        .where(Recipe.id == recipe_id)
    )
    final_recipe = result.scalars().first()
    return final_recipe

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Recipe).where(Recipe.id == recipe_id))
    recipe = result.scalars().first()

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    
    if recipe.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this recipe")
    
    recipe.deleted_at = datetime.utcnow()
    db.add(recipe)
    await db.commit()
    return {"message": "Recipe deleted successfully"}
