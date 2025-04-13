from fastapi_cache import FastAPICache

async def clear_user_detail_cache(user_id: str):
    path = f"/api/v1/users/{user_id}"
    cache_key = f"user-detail:{path}"

    print(f"🧼 Clearing cache for: {cache_key}")
    await FastAPICache.clear_key(cache_key)
