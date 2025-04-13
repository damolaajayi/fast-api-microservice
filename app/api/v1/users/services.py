from fastapi import HTTPException
from fastapi_cache import FastAPICache
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from uuid import UUID, uuid4
from typing import List, Optional
from app.api.v1.users.models import GenderEnum, RoleEnum, User
from app.api.v1.users.schemas import UserCreate, UserListResponse, UserResponse, UserUpdate
from app.schemas.response import APIResponse
from app.services.auth.hashing import hash_password, verify_password
from app.utils.cache_helpers import clear_user_detail_cache


async def get_all_users(db: AsyncSession, 
                        limit: int, 
                        offset:int, 
                        gender: Optional[GenderEnum],
                        role: Optional[RoleEnum],
                        search: Optional[str]) -> APIResponse[UserListResponse]:
    query = select(User)
    if gender:
        query = query.where(User.gender == gender)
    if role:
        query = query.where(User.roles.any(role))
        
    if search:
        query = query.where(
            or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )
        
    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar()
    result = await db.execute(query.offset(offset).limit(limit))
    users = result.scalars().all()
    response = UserListResponse(
        data=[UserResponse.from_orm(user) for user in users],
        total=total,
        limit=limit,
        offset=offset
    )
    return APIResponse(
        status_code=200,
        message="Users retrieved successfully",
        data=response
    )

async def get_user_by_id(user_id: UUID, db: AsyncSession) -> UserResponse:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_orm(user) 


async def register_user(user: UserCreate, db: AsyncSession):
     existing_user = await get_user_by_username(db, user.username)
     if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

     existing_email = await get_user_by_email(db, user.email)
     if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
     new_user = User(
          username=user.username,
          first_name=user.first_name,
          last_name=user.last_name,
          middle_name=user.middle_name,
          gender= user.gender,
          password=hash_password(user.password),
          roles=user.roles,
          email=user.email
     )
     
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
     await FastAPICache.clear(namespace="users")
     await clear_user_detail_cache(str(user_id))
     return {"detail": f"User with id {user_id} deleted successfully"}


     
async def update_user(user_id: UUID, user_update: UserUpdate, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
          raise HTTPException(404, detail="User not found")
    for key, value in user_update.model_dump(exclude_unset=True).items():
          setattr(user, key, value)
    await db.commit()
    await FastAPICache.clear(namespace="users")
    await clear_user_detail_cache(str(user_id))
    await db.refresh(user)
    return user


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

