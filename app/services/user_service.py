from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from app.schemas.user_schema import UserCreate, UserUpdate
from app.models.user import User
from uuid import UUID, uuid4
from typing import List


async def get_all_users(db: AsyncSession):
     result = await db.execute(select(User))
     return result.scalars().all()


async def register_user(user: User, db: AsyncSession):
     new_user = User(**user.dict())
     db.add(new_user)
     await db.commit()
     await db.refresh(new_user)
     return new_user


async def remove_user(user_id: UUID, db: AsyncSession):
     result = await db.execute(select(User).where(User.id == user_id))
     user = result.scalars().first()
     if not user:
          raise HTTPException(404, detail="User not found")
     await db.delete(user)
     await db.commit()
     return {"detail": f"User with id {user_id} deleted successfully"}
     
async def update_user(user_id: UUID, user_update: UserUpdate, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
          raise HTTPException(404, detail="User not found")
    for key, value in user_update.model_dump(exclude_unset=True).items():
          setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user