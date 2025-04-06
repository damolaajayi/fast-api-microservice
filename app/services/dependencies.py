import time
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from app.api.v1.users.services import get_user_by_username
from app.services.auth.jwt import SECRET_KEY, ALGORITHM
from app.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")

bearer_scheme = HTTPBearer()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},)
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


def send_welcome_email(email: str, username: str):
    # Placeholder for sending email logic
    print(f"Starting to send email to {email}")
    time.sleep(5)  # simulate delay
    print(f"Email sent to {email}")
    