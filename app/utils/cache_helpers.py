from fastapi_cache import FastAPICache

async def clear_user_detail_cache(user_id: str):
    path = f"/api/v1/users/{user_id}"
    cache_key = f"fastapi-cache:user-detail:{path}"

    print(f"🧼 Clearing cache for: {cache_key}")
    redis_backend = FastAPICache.get_backend()
    await redis_backend.redis.delete(cache_key)
