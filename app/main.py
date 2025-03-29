from fastapi import FastAPI
from app.api.v1.api_router import router as api_router
app = FastAPI(title="My First FastAPI",version=
            "0.1",description="This is my first FastAPI project")

app.include_router(api_router, prefix="/api/v1")



