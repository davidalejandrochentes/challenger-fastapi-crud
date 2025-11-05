from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from datetime import datetime

from core.database import SessionLocal
from models.review import Review
from models.recipe import Recipe
from schemas.review import Review as ReviewSchema, ReviewCreate, ReviewUpdate
from routers.auth import get_current_user, get_db
from models.user import User

router = APIRouter()

@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Recipe).where(Recipe.id == review.recipe_id))
    recipe = result.scalars().first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    new_review = Review(
        rating=review.rating,
        comment=review.comment,
        recipe_id=review.recipe_id,
        user_id=current_user.id
    )
    db.add(new_review)
    await db.flush()
    review_id = new_review.id
    await db.commit()

    result = await db.execute(
        select(Review).options(selectinload(Review.user)).where(Review.id == review_id)
    )
    final_review = result.scalars().first()
    return final_review

@router.get("/", response_model=List[ReviewSchema])
async def read_all_reviews(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Review).options(selectinload(Review.user))
    )
    reviews = result.scalars().all()
    return [review for review in reviews if review.user is not None]

@router.get("/recipe/{recipe_id}", response_model=List[ReviewSchema])
async def read_reviews_for_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Review).options(selectinload(Review.user)).where(Review.recipe_id == recipe_id)
    )
    reviews = result.scalars().all()
    return [review for review in reviews if review.user is not None]

@router.get("/{review_id}", response_model=ReviewSchema)
async def read_review(review_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Review).options(selectinload(Review.user)).where(Review.id == review_id)
    )
    review = result.scalars().first()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=ReviewSchema)
async def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalars().first()

    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    
    if review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this review")
    
    review_data = review_update.dict(exclude_unset=True)
    for key, value in review_data.items():
        setattr(review, key, value)
    
    await db.commit()

    result = await db.execute(
        select(Review).options(selectinload(Review.user)).where(Review.id == review_id)
    )
    final_review = result.scalars().first()
    return final_review

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalars().first()

    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    
    if review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this review")
    
    review.deleted_at = datetime.utcnow()
    db.add(review)
    await db.commit()
    return {"message": "Review deleted successfully"}
