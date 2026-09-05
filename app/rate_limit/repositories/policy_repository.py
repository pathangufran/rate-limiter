from typing import Any
from sqlalchemy import delete,select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.rate_limit_policy import RateLimitPolicy

class PolicyRepository:

    async def create(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        data: dict[str, Any],
    ) -> RateLimitPolicy:

        policy = RateLimitPolicy(
            tenant_id=tenant_id,
            **data,
        )

        await db.add(policy)
        await db.flush()
        await db.refresh(policy)

        return policy

    async def get_by_id(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        policy_id: int,
    ) -> RateLimitPolicy | None:

        result = await db.execute(
            select(RateLimitPolicy).where(
                RateLimitPolicy.id == policy_id,
                RateLimitPolicy.tenant_id == tenant_id,
            )
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        policy_id: int,
        data: dict[str, Any],
    ) -> RateLimitPolicy:

        policy = await self.get_by_id(
            db=db,
            tenant_id=tenant_id,
            policy_id=policy_id,
        )

        for field,value in data.items():
            setattr(policy,field,value)

        await db.flush()
        await db.refresh(policy)

        return policy

    async def delete(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        policy_id: int,
    ) -> None:

        policy = await self.get_by_id(
            db=db,
            tenant_id=tenant_id,
            policy_id=policy_id,
        )

        await db.delete(policy)
        await db.flush()
