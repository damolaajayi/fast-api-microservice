from fastapi import APIRouter
from services.user_service import get_users

router = APIRouter()

@router.get("")
def read_users():
    return get_users()