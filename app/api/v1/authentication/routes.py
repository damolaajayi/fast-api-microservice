from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.authentication.schemas import LoginRequest, RefreshRequest, TokenPairResponse
from app.api.v1.authentication.services import authenticate_user
from app.db.session import get_db
from app.schemas.response import APIResponse
from app.schemas.token import TokenResponse
from app.services.auth.jwt import create_access_token, create_refresh_token, verify_refresh_token


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

