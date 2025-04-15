from datetime import datetime, timedelta
import os
from jose import jwt

from app.services.auth.jwt import ALGORITHM



RESET_SECRET_KEY = os.getenv("RSET_SECRET_KEY", "reset_secret_key")

def create_reset_token(email: str, expires_minutes: int =15) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {
        "sub": email,
        "exp": expire

    }
    return jwt.encode(payload, RESET_SECRET_KEY, algorithm=ALGORITHM)


def verify_reset_token(token: str) -> dict:
    from jose import JWTError
    
    try:
        payload = jwt.decode(token, RESET_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        return None
