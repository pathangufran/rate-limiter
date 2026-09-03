import json
from app.rate_limit.cache import RuleCache

class RedisRuleCache(RuleCache):

    def __init__(self,redis,):
        self.redis = redis

    async def get(self,key: str):

        value = await self.redis.get(key)

        if value is None:
            return None
        
        if isinstance(value,bytes):
            value = value.decode("utf-8")

        return json.loads(value)

    async def set(
        self,key: str,value,*,ttle: int,
    ) -> None:

        payload = json.dumps(
            value,
            separators=(",",":"),
        )

        await self.redis.set(key,payload,ex=ttle,)

    async def delete(self,key: str,) -> None:

        await self.redis.delete(key)