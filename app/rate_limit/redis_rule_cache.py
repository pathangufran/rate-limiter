import json
from app.rate_limit.cache import RuleCache
from app.rate_limit.cache_models import CachedRule

class RedisRuleCache(RuleCache):

    def __init__(self,redis,):
        self.redis = redis

    async def get(
        self,
        key: str
    ) -> list[CachedRule] | None:

        value = await self.redis.get(key)

        if value is None:
            return None
        
        if isinstance(value,bytes):
            value = value.decode("utf-8")

        payload = json.loads(value)
        rules = payload.get("rules",[])

        return [
            CachedRule.from_dict(rule)
            for rule in rules
        ]

    async def set(
        self,
        key: str,
        rules:list[CachedRule],
        value,
        *,
        ttl: int,
    ) -> None:

        payload = {
            "rues": [
                rule.to_dict()
                for rule in rules
            ]
        }

        serialized = json.dumps(
            payload,
            separators=(",", ":"),
        )

        await self.redis.set(
            key,
            serialized,
            ex=ttl,
        )

    async def delete(self,key: str,) -> None:

        await self.redis.delete(key)