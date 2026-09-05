from sqlalchemy.ext.asyncio import AsyncSession
from app.rate_limit.caches.invalidation import (
    RuleCacheInvalidationService,
)
from app.rate_limit.repositories.policy_repository import (
    PolicyRepository,
)

class PolicyService:

    def __init__(
        self,
        repository: PolicyRepository,
        cache_invalidation: RuleCacheInvalidationService,   
    ):
        self.repository = repository
        self.cache_invalidation = cache_invalidation

    async def create_policy(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        data,
    ): 
        policy = await self.repository.create(
            db=db,
            tenant_id=tenant_id,
            data=data,
        )

        await db.commit()
        await self.cache_invalidation.invalidate_tenant(
            tenant_id=tenant_id,
        )

        return policy

    async def update_policy(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        policy_id: int,
        data,
    ):
        policy = await self.repository.update(
            db=db,
            tenant_id=tenant_id,
            policy_id=policy_id,
            data=data,
        )

        await db.commit()
        await self.cache_invalidation.invalidate_tenant(
            tenant_id=tenant_id,
        )

        return policy

    async def delete_policy(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        policy_id: int,
    ):
        await self.repository.delete(
            db=db,
            tenant_id=tenant_id,
            policy_id=policy_id,
        )

        await db.commit()
        await self.cache_invalidation.invalidate_tenant(
            tenant_id=tenant_id,
        )