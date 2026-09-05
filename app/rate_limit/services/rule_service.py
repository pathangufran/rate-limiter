from sqlalchemy.ext.asyncio import AsyncSession
from app.rate_limit.caches.invalidation import (
    RuleCacheInvalidationService,
)
from app.rate_limit.repositories import (
    rule_repository,
)

class RuleService:

    def __init__(
        self,
        repository: rule_repository,
        cache_invalidation: RuleCacheInvalidationService,
    ):
        self.repository = repository
        self.cache_invalidation = cache_invalidation

    async def create_rule(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        data,
    ): 
        rule = await self.repository.create(
            db=db,
            tenant_id=tenant_id,
            data=data,
        )

        await db.commit()
        await self.cache_invalidation.invalidate_tenant(
            tenant_id=tenant_id,
        )

        return rule

    async def update_rule(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        rule_id: int,
        data,
    ):
        rule = await self.repository.update(
            db=db,
            tenant_id=tenant_id,
            rule_id=rule_id,
            data=data,
        )

        await db.commit()
        await self.cache_invalidation.invalidate_tenant(
            tenant_id=tenant_id,
        )

        return rule

    async def delete_url(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        rule_id: int,
    ):
        await self.repository.delete(
            db=db,
            tenant_id=tenant_id,
            rule_id=rule_id,
        )

        await db.commit()
        await self.cache_invalidation.invalidate_tenant(
            tenant_id=tenant_id,
        )