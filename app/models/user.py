from sqlalchemy import Column, String, Enum as SQLEnum,  ARRAY
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional, List
import uuid
from pydantic import BaseModel
from enum import Enum

from app.db.database import Base

class GenderEnum(str, Enum):
    male = "male"
    female = "female"

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    student = "student"
    
class User(Base):
    __tablename__ = "users"
    id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    gender= Column(String, nullable=False)
    roles= Column(ARRAY(SQLEnum(RoleEnum)))
    
# class UserUpdateRequest(BaseModel):
#     first_name: Optional[str] = None
#     last_name: Optional[str] = None
#     middle_name: Optional[str] = None
#     roles: Optional[List[Role]] = None