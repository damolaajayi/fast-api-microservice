from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field

PasswordStr = Annotated[str, Field(min_length=8)]

class LoginRequest(BaseModel):
    username: str 
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime
    
class TokenPairResponse(TokenResponse):
    refresh_token: str
    
class RefreshRequest(BaseModel):
    refresh_token: str
    
class RequestPasswordReset(BaseModel):
    email: EmailStr
    
class ConfirmPasswordReset(BaseModel):
    token: str
    new_password: PasswordStr
    
