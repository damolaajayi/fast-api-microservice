from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.api.v1.users.models import GenderEnum, RoleEnum, User
from app.api.v1.users.schemas import UserCreate, UserListResponse, UserOut, UserResponse, UserUpdate
from app.api.v1.users.services import get_all_users, get_user_by_id, register_user, remove_user, update_user
from app.core.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.response import APIResponse
from app.schemas.token import TokenResponse
from app.services.dependencies import get_current_user
from app.db.session import get_db
from uuid import UUID

router = APIRouter()

@router.get("", response_model=APIResponse[UserListResponse], status_code=status.HTTP_200_OK) 
async def retrieve_users(db: AsyncSession =  Depends(get_db),
                         limit : int = Query(10),
                         offset: int = Query(0),
                         gender: Optional[GenderEnum] = None,
                         role: Optional[RoleEnum] = None,
                         search: Optional[str] = None,
                         current_user: User = Depends(get_current_user))-> APIResponse[UserListResponse]:
    return await get_all_users(db, limit, offset, gender, role, search)
    

@router.get("/{user_id}", response_model=APIResponse[UserResponse], status_code=status.HTTP_200_OK) 
async def retrieve_user(user_id: UUID, db: AsyncSession =  Depends(get_db), current_user: User = Depends(get_current_user))-> APIResponse[UserResponse]:
    get_users = await get_user_by_id(user_id,db)
    logger.info("This should show up in the terminal and in logs/app.log")
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="User retrieved successfully",
        data=get_users
    )

@router.post("", response_model=APIResponse[UserOut], status_code=status.HTTP_201_CREATED)
async def add_user(user: UserCreate, db: AsyncSession =  Depends(get_db)) -> APIResponse[list[UserOut]]:
    new_user = await register_user(user, db)
    return APIResponse(
        status_code=status.HTTP_201_CREATED,
        message="User created successfully",
        data=new_user
    )
    
       
@router.put("/{user_id}", response_model=UserResponse)
async def edit_user(user_id: UUID, user: UserUpdate, db: AsyncSession =  Depends(get_db)):
    return await update_user(user_id, user, db)


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, db: AsyncSession =  Depends(get_db)):
    return await remove_user(user_id, db)



