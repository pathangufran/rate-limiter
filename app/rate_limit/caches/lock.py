from app.rate_limit.cache_keys import (
    build_rule_cache_lock_key,
)

class RuleCacheLock:

    def __init__(
        self,
        redis,
        *,
        lock_ttl: int = 5,
    ):
        if lock_ttl <= 0:
            raise ValueError(
                "lock_ttl must be greater than zero"
            )

        self.redis = redis
        self.lock_ttl = lock_ttl

    async def acquire(
        self,
        *,
        tenant_id: int,
        generation: int,
        method: str,
        endpoint: str,
        identity_type: str,
        identity_id: str,
    ) -> bool:

        key = build_rule_cache_lock_key(
            tenant_id=tenant_id,
            generation=generation,
            method=method,
            endpoint=endpoint,
            identity_type=identity_type,
            identity_id=identity_id,
        )

        result = await self.redis.set(
            key,
            "1",
            nx=True,
            ex=self.lock_ttl,
        )

        return bool(result)

    async def release(
        self,
        *,
        tenant_id: int,
        generation: int,
        method: str,
        endpoint: str,
        identity_type: str,
        identity_id: str,
    ) -> None:

        key = build_rule_cache_lock_key(
            tenant_id=tenant_id,
            generation=generation,
            method=method,
            endpoint=endpoint,
            identity_type=identity_type,
            identity_id=identity_id,
        )

        await self.redis.delete(key)