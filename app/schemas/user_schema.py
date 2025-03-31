from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from app.models.user import GenderEnum, RoleEnum


class UserBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    gender: GenderEnum
    roles: List[RoleEnum]
    
class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    gender: Optional[GenderEnum] = None 
    roles: Optional[List[RoleEnum]] = None

class UserResponse(UserBase):
    id: UUID
    
    class Config:
        from_attributes = True