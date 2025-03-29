from fastapi import APIRouter, HTTPException
from app.services.user_service import get_users, register_user, remove_user
from app.models.user import User
from uuid import UUID

router = APIRouter()

@router.get("")
async def retrieve_users():
    return get_users()

@router.post("")
async def add_user(user: User):
    return register_user(user)

@router.delete("/{user_id}")
async def delete_user(user_id: UUID):
    return remove_user(user_id)
