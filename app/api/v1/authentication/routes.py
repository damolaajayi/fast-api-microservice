from app.api.v1.users.services import get_user_by_email
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth.hashing import hash_password
from app.services.auth.password_reset import create_reset_token, verify_reset_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.authentication.schemas import ConfirmPasswordReset, LoginRequest, RefreshRequest, RequestPasswordReset, TokenPairResponse
from app.api.v1.authentication.services import authenticate_user
from app.db.session import get_db
from app.schemas.response import APIResponse
from app.schemas.token import TokenResponse
from app.services.auth.jwt import create_access_token, create_refresh_token, verify_refresh_token
from app.workers.tasks import send_password_reset_email_task


router = APIRouter()


@router.post("/login", response_model=APIResponse[TokenPairResponse], status_code=status.HTTP_200_OK)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db))-> APIResponse[TokenResponse]:
    user = await authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token, expire = create_access_token(data={"sub": user.username, "roles": user.roles})
    refreshtoken = create_refresh_token(data={"sub": user.username})
    response = TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_at=expire
    )
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Token returned successfully",
        data=TokenPairResponse(
            access_token=access_token,
            token_type="bearer",
            expires_at=expire,
            refresh_token=refreshtoken
        )
    )


@router.post("/refresh", response_model=APIResponse[TokenResponse], status_code=status.HTTP_200_OK)
async def refresh_token(payload: RefreshRequest):
    payload_data = verify_refresh_token(payload.refresh_token)
    if not payload_data:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    access_token, expires_at = create_access_token(data={"sub": payload_data["sub"], "roles": payload_data.get("roles", [])})
    return APIResponse(
        status_code=200,
        message="Access token refreshed successfully",
        data=TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_at=expires_at
        )
    )
    
    
@router.post("/request-password-reset", status_code=status.HTTP_200_OK)
async def request_password_reset(payload: RequestPasswordReset, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    token = create_reset_token(user.email)
    reset_link = f"http://example.com/reset-password?token={token}"
    send_password_reset_email_task.delay(user.email, reset_link)
    
    return APIResponse(message="Password reset email sent")
    
@router.post("/confirm-password-reset", status_code=status.HTTP_200_OK)
async def confirm_password_reset(payload: ConfirmPasswordReset, db: AsyncSession = Depends(get_db)):
    email = verify_reset_token(payload.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.password = hash_password(payload.new_password)
    await db.commit()
    return APIResponse(messsage="Password reset successfully")

