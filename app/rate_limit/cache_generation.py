from app.rate_limit.cache_keys import (
    build_rule_generation_key,
)

class RuleCacheGeneration:

    def __init__(self,redis):
        self.redis = redis

    async def get(
        self,
        *,
        tenant_id: int,
    ) -> int:

        key = build_rule_generation_key(
            tenant_id=tenant_id,
        )
        value = await self.redis.get(key)

        if value is None:
            return 1
        if isinstance(value,bytes):
            value = value.decode("utf-8")

        return int(value)

    async def invalidate(
        self,
        *,
        tenant_id: int,
    ) -> int:

        key = build_rule_generation_key(
            tenant_id=tenant_id,
        )

        return await self.redis.incr(key)
