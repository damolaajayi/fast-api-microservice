# app/core/sentry_context.py

import sentry_sdk
from jose import jwt, JWTError
from fastapi import Request
from app.db.session import AsyncSessionLocal
from app.api.v1.users.services import get_user_by_username
from app.services.auth.jwt import SECRET_KEY, ALGORITHM
from fastapi.security.utils import get_authorization_scheme_param

async def sentry_context_middleware(request: Request, call_next):
    with sentry_sdk.configure_scope() as scope:
        scope.set_context("request", {
            "url": str(request.url),
            "method": request.method,
            "headers": dict(request.headers),
        })

        try:
            auth = request.headers.get("Authorization")
            scheme, token = get_authorization_scheme_param(auth)
            if scheme.lower() == "bearer":
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username = payload.get("sub")
                if username:
                    async with AsyncSessionLocal() as session:
                        user = await get_user_by_username(session, username)
                        if user:
                            scope.user = {
                                "id": str(user.id),
                                "email": user.email,
                                "username": user.username
                            }
        except JWTError:
            pass  # token invalid
        except Exception as e:
            print("Sentry user context error:", e)

    response = await call_next(request)
    return response
