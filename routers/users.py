from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime

from core.database import SessionLocal
from models.user import User
from schemas.user import User as UserSchema, UserUpdate, UserPublic
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/", response_model=List[UserPublic])
async def read_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserSchema)
async def update_user_me(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_data = user_update.dict(exclude_unset=True)
    
    for key, value in user_data.items():
        setattr(current_user, key, value)
        
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.deleted_at = datetime.utcnow()
    db.add(current_user)
    await db.commit()
    return {"message": "User deleted successfully"}

@router.get("/{username}", response_model=UserSchema)
async def read_user(username: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None or user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
