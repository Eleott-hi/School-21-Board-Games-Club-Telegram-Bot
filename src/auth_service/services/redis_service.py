from config import REDIS_SERVICE_HOST, REDIS_SERVICE_PORT
import redis.asyncio as redis


class RedisService:

    def __init__(self):
        self.redis = redis.Redis(host=REDIS_SERVICE_HOST, port=int(REDIS_SERVICE_PORT))

    async def set(self, key: str, value: str, ttl=None):
        await self.redis.set(name=key, value=int(value), ex=ttl)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)
