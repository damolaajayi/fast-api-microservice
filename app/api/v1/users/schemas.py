from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

from app.api.v1.users.models import GenderEnum, RoleEnum



class UserBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    gender: GenderEnum
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    roles: List[RoleEnum]
    
class UserOut(BaseModel):
    id: UUID
    username: str
    email: str
    roles: List[RoleEnum]

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    gender: Optional[GenderEnum] = None 

class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    gender: GenderEnum
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    roles: List[RoleEnum]

    
    class Config:
        from_attributes = True
        
class UserListResponse(BaseModel):
    data: List[UserResponse]
    total: int
    limit: int
    offset: int