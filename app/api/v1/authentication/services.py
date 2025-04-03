from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.users.services import get_user_by_username
from app.services.auth.hashing import verify_password



async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if user and verify_password(password, user.password):
        return user
    return None