from app.rate_limit.cache import RuleCache
from app.rate_limit.cache_keys import (
    build_rule_cache_key,
)
from app.rate_limit.cache_models import (
    CachedRule,
)

class RuleCacheService:

    def __init__(
        self,
        cache: RuleCache,
        *,
        ttl: int = 60,
    ):
        self.cache = cache
        self.ttl = ttl

    async def get(
        self,
        *,
        tenant_id: int,
        method: str,
        endpoint: str,
        identity_type: str,
        identity_id: str,
    ) -> list[CachedRule] | None:
         
        key = build_rule_cache_key(
            tenant_id=tenant_id,
            method=method,
            endpoint=endpoint,
            identity_type=identity_type,
            identity_id=identity_id,
        )

        return await self.cache.get(key)

    async def set(
        self,
        *,
        tenant_id: int,
        method: str,
        endpoint: str,
        identity_type: str,
        identity_id: str,
        rules: list[CachedRule],
    ) -> None:
        
        key = build_rule_cache_key(
            tenant_id=tenant_id,
            method=method,
            endpoint=endpoint,
            identity_type=identity_type,
            identity_id=identity_id,
        )

        await self.cache.set(
            key,
            {"rules": rules},
            ttl=self.ttl,
        )

    async def delete(
        self,
        *,
        tenant_id: int,
        method: str,
        endpoint: str,
        identity_type: str,
        identity_id: str,   
    ) -> None:
        key = build_rule_cache_key(
            tenant_id=tenant_id,
            method=method,
            endpoint=endpoint,
            identity_type=identity_type,
            identity_id=identity_id,
        )

        await self.cache.delete(key)