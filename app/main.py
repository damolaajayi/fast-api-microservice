from fastapi import FastAPI
from api.v1.api_router import router as api_router
import sys

app = FastAPI(title="My First FastAPI",version=
            "0.1",description="This is my first FastAPI project")

app.include_router(api_router, prefix="/api/v1")

# 🧪 Debug route to print all loaded routes
@app.get("/__debug_routes__")
def debug_routes():
    return [route.path for route in app.routes]

for route in app.routes:
    print(route.path)


