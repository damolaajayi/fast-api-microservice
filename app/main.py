from app.core.cache import init_cache
from app.db.session import get_db
from app.api.v1.users.models import User
import asyncio
from app.api.api_router import router as api_router
from app.core.expection_handlers import register_exception_handlers
from app.schemas.response import ErrorResponse
from app.core.middleware import LoggingMiddleware
from app.db.session import engine
from app.db.session import Base



app = FastAPI(title="My First FastAPI",version=
            "0.1",description="This is my first FastAPI project")


@app.on_event("startup")
async def startup():
    await init_cache()



app.add_middleware(LoggingMiddleware)
register_exception_handlers(app)

app.include_router(api_router, prefix="/api/v1")



