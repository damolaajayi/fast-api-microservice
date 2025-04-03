from fastapi import APIRouter
from app.api.v1.users.routes import router as user_router
from app.api.v1.authentication.routes import router as auth_router


router = APIRouter()
router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])