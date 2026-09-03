from app.rate_limit.cache_mapper import (
    rule_to_cached_rule,
)
from app.rate_limit.rule_cache_service import (
    RuleCacheService,
)
from app.rate_limit.resolved_rule import (
    cached_rule_to_resolved_rule,
)

class RuleResolver:

    def __init__(
        self,
        repository,
        cache_service: RuleCacheService,
    ):
        self.repository = repository
        self.cache_service = cache_service

    async def resolve(
        self,
        *,
        tenant_id: int,
        method: str,
        endpoint: str,
        identity_type: str,
        identity_id: str,
    ):
        cached_rules = (
            await self.cache_service.get(
                tenant_id=tenant_id,
                method=method,
                endpoint=endpoint,
                identity_type=identity_type,
                identity_id=identity_id,
            )
        )
        if cached_rules is not None:
            return [
                cached_rule_to_resolved_rule(
                    rule
                )
                for rule in cached_rules
            ]

        resolved_rules = (
            await self.repository.resolve(
                tenant_id=tenant_id,
                method=method,
                endpoint=endpoint,
                identity_type=identity_type,
                identity_id=identity_id,
            )
        )
        cached_rules = [
            rule_to_cached_rule(
                resolved_rule
            )
            for resolved_rule in resolved_rules
        ]
        await self.cache_service.set(
            tenant_id=tenant_id,
            method=method,
            endpoint=endpoint,
            identity_type=identity_type,
            identity_id=identity_id,
            rules=cached_rules,
        )

        return resolved_rules