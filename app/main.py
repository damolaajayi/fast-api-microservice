from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.api_router import router as api_router
from app.core.expection_handlers import register_exception_handlers
from app.schemas.response import ErrorResponse
from app.core.middleware import LoggingMiddleware
app = FastAPI(title="My First FastAPI",version=
            "0.1",description="This is my first FastAPI project")




app.add_middleware(LoggingMiddleware)
register_exception_handlers(app)

app.include_router(api_router, prefix="/api/v1")



