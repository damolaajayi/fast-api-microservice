import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.core.logger import logger



class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start

        logger.info(f"{request.method} {request.url.path}"
                    f"→ {response.status_code} ({duration:.2f}s)")
        return response