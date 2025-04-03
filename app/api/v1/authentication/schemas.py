from datetime import datetime
from pydantic import BaseModel


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