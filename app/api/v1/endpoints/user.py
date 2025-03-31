from fastapi import APIRouter, Depends, HTTPException
from app.schemas import user_schema
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import get_all_users, register_user, remove_user, update_user
from app.models.user import User
from app.db.database import get_db
from uuid import UUID

router = APIRouter()

@router.get("", response_model=list[user_schema.UserResponse])
async def retrieve_users(db: AsyncSession =  Depends(get_db)):
    return await get_all_users(db)

@router.post("", response_model=user_schema.UserResponse)
async def add_user(user: user_schema.UserCreate, db: AsyncSession =  Depends(get_db)):
    return await register_user(user, db)

@router.put("/{user_id}", response_model=user_schema.UserResponse)
async def edit_user(user_id: UUID, user: user_schema.UserUpdate, db: AsyncSession =  Depends(get_db)):
    return await update_user(user_id, user, db)


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, db: AsyncSession =  Depends(get_db)):
    return await remove_user(user_id, db)
