from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
from fastapi import Request, Response

def custom_cache_key_builder(func, namespace: str = "", request: Request = None, response: Response = None, args: tuple = (),
    kwargs: dict = {}):
    path = request.url.path
    query_items = sorted(request.query_params.items())
    query_str = "&".join(f"{k}={v}" for k, v in query_items)

    if query_items:
        # Example: users:/api/v1/users?limit=10&offset=0
        key = f"{namespace}:{path}?{query_str}"
    else:
        # Example: users:/api/v1/users/123e4567-e89b-12d3-a456-426614174000
        key = f"{namespace}:{path}"

    print(f"🧠 Cache key: {key}")
    return key



async def init_cache():
    redis_client = redis.Redis(host="redis", port=6379, db=2)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache", key_builder=custom_cache_key_builder)