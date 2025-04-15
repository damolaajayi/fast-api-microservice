from app.core.cache import init_cache
from app.core.security_context import sentry_context_middleware
from fastapi import FastAPI
from app.db.session import get_db
from app.api.v1.users.models import User
import asyncio
from app.api.api_router import router as api_router
from app.core.expection_handlers import register_exception_handlers
from app.schemas.response import ErrorResponse
from app.core.middleware import LoggingMiddleware
from app.db.session import engine
from app.db.session import Base
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware



app = FastAPI(title="My First FastAPI",version=
            "0.1",description="This is my first FastAPI project")


@app.on_event("startup")
async def startup():
    await init_cache()


@app.get("/debug-sentry")
async def trigger_error():
    division_by_zero = 1 / 0


app.add_middleware(LoggingMiddleware)
register_exception_handlers(app)
app.add_middleware(SentryAsgiMiddleware)
app.middleware("http")(sentry_context_middleware)

app.include_router(api_router, prefix="/api/v1")



