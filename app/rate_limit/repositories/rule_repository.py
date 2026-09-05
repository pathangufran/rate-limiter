from typing import Any
from sqlalchemy import date,select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.rate_limit_rule import RateLimitRule

class RuleReposity:

    async def create(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        data: dict[str, Any],
    ) -> RateLimitRule:

        rule = RateLimitRule(
            tenant_id=tenant_id,
            **data,
        )

        db.add(rule)
        await db.flush()
        await db.refresh(rule)

        return rule

    async def get_by_id(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        rule_id: int,
    ) -> RateLimitRule | None:

        result = await db.execute(
            select(RateLimitRule).where(
                RateLimitRule.id == rule_id,
                RateLimitRule.tenant_id == tenant_id,
            )
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        rule_id: int,
        data: dict[str, Any],
    ) -> RateLimitRule:

        rule = await self.get_by_id(
            db=db,
            rule_id=rule_id,
            tenant_id=tenant_id,
        )
        if rule is None:
            raise ValueError(
                f"Rate-limit rule {rule_id} not found"
            )

        for field,value in data.items():
            setattr(rule,field,value)

        await db.flush()
        await db.refresh(rule)

        return rule

    async def delete(
        self,
        *,
        db: AsyncSession,
        tenant_id: int,
        rule_id: int,
    ) -> None:

        rule = await self.get_by_id(
            db=db,
            rule_id=rule_id,
            tenant_id=tenant_id,
        )
        if rule is None:
            raise ValueError(
                f"Rate-limit rule {rule_id} not found"
            )

        await db.delete(rule)
        await db.flush()