from fastapi import APIRouter, Depends, HTTPException
from app.services.user_service import get_all_users, get_users_db, register_user, remove_user, update_user
from app.models.user import User, UserUpdateRequest
from uuid import UUID

router = APIRouter()

@router.get("", response_model=list[User])
async def retrieve_users(db=Depends(get_users_db)):
    return get_all_users(db)

@router.post("")
async def add_user(user: User, db=Depends(get_users_db)):
    return register_user(user, db)

@router.put("/{user_id}")
async def edit_user(user_id: UUID, user_update: UserUpdateRequest, db=Depends(get_users_db)):
    return update_user(user_id, user_update, db)


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, db=Depends(get_users_db)):
    return remove_user(user_id, db)
