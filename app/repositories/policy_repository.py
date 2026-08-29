from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.rate_limit_policy import RateLimitPolicy

class PolicyRepository:

    def __init__(self,session: AsyncSession):
        self.session = session

    async def create(
        self,
        policy: RateLimitPolicy,
    ) -> RateLimitPolicy:

        self.session.add(policy)
        await self.session.flush()

        return policy

    async def get_by_id(
        self,
        policy_id: UUID,
    ) -> RateLimitPolicy | None:

        result = await self.session.execute(
            select(RateLimitPolicy).where(
                RateLimitPolicy.id == policy_id
            )
        )

        return result.scalar_one_or_none()

    async def list(self,) -> list[RateLimitPolicy]:

        result = await self.session.execute(
            select(RateLimitPolicy)
            .order_by(
                RateLimitPolicy.created_at().desc()
            )
        )

        return list(result.scalars().all())