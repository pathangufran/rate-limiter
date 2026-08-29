from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.rate_limit_rule import RateLimitRule

class RuleRepository:

    def __init__(self,session: AsyncSession):
        self.session = session

    async def create(
        self,
        rule: RateLimitRule,
    ) -> RateLimitRule:

        self.session.add(rule)
        await self.session.flush()

        return rule

    async def get_by_id(
        self,
        rule_id: UUID,
    ) -> RateLimitRule | None:

        result = await self.session.execute(
            select(RateLimitRule).where(
                RateLimitRule.id == rule_id
            )
        )

        return result.scalar_one_or_none()

    async def list(self,) -> list[RateLimitRule]:

        result = await self.session.execute(
            select(RateLimitRule)
            .order_by(
                RateLimitRule.priority.desc(),
                RateLimitRule.created_at().desc(),
            )
        )

        return list(result.scalars().all())