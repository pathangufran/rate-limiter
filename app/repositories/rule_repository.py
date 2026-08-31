from uuid import UUID
from sqlalchemy import or_,select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
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
            select(RateLimitRule).options(
                selectinload(
                    RateLimitRule.policy
                )
            )
            .where(
                RateLimitRule.id == rule_id
            )
        )

        return result.scalar_one_or_none()

    async def list_rules(self,) -> list[RateLimitRule]:

        result = await self.session.execute(
            select(RateLimitRule)
            .options(
                selectinload(
                    RateLimitRule.policy
                )
            )
            .order_by(
                RateLimitRule.priority.desc(),
                RateLimitRule.created_at().desc(),
            )
        )

        return list(result.scalars().all())

    async def find_applicable(
        self,
        *,
        tenant_id: UUID,
        plan_id: UUID | None,
        user_id: UUID | None,
        api_key_id: UUID | None,
        endpoint_id: UUID | None,
    ) -> list[RateLimitRule]:

        conditions = [
            RateLimitRule.scope == "GLOBAL",
        ]
        conditions.append(
            RateLimitRule.scope == "IP"
        )
        if plan_id is not None:
            conditions.append(
                (
                    RateLimitRule.scope == "PLAN"
                )
                & (
                    RateLimitRule.plan_id == plan_id
                )
            )
            conditions.append(
                (
                    RateLimitRule.scope == "TENANT"
                )
                & (
                    RateLimitRule.tenant_id == tenant_id
                )
            )
            if user_id is not None:
                conditions.append(
                    (
                        RateLimitRule.scope == "USER"
                    )
                    & (
                        RateLimitRule.user_id == user_id
                    )
                )
            if api_key_id is not None:
                conditions.append(
                    (
                        RateLimitRule.scope == "API_KEY"
                    )
                    & (
                        RateLimitRule.api_key_id == api_key_id
                    )
                )

            if endpoint_id is not None:
                conditions.append(
                    (
                        RateLimitRule.scope == "ENDPOINT"
                    )
                    & (
                        RateLimitRule.endpoint_id == endpoint_id
                    )
                )

        result = await self.session.execute(
            select(RateLimitRule)
            .options(
                selectinload(
                    RateLimitRule.policy
                )
            )
            .where(
                RateLimitRule.is_active.is_(True)
            )
            .where(
                or_(*conditions)
            )
            .order_by(
                RateLimitRule.priority.desc()
            )
        )

        return list(result.scalars().all())
        

