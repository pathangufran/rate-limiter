from uuid import UUID
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.admin.rule_schemas import (
    RuleCreateRequest,
    RuleUpdateRequest,
)
from app.models.rate_limit_rule import RateLimitRule
from app.repositories.policy_repository import PolicyRepository
from app.repositories.rule_repository import RuleRepository

class RuleService:

    def __init__(self,session: AsyncSession):
        self.session = session
        self.repository = RuleRepository(session)
        self.policy_repository = PolicyRepository(session)

    async def create(
        self,
        payload: RuleCreateRequest,
    ) -> RateLimitRule:

        policy = await self.repository.get_by_id(
            payload.policy_id
        )
        if policy is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Policy does not exist",
            )
        if not policy.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot create rule for disabled policy",
            )

        rule = RateLimitRule(
            policy_id=payload.policy_id,
            scope=payload.scope.value,
            plan_id=payload.plan_id,
            tenant_id=payload.tenant_id,
            user_id=payload.user_id,
            api_key_id=payload.api_key_id,
            endpoint_id=payload.endpoint_id,
            priority=payload.priority,
        )

        await self.repository.create(rule)
        await self.sesson.commit()

        return rule

    async def get(self,rule_id: UUID) -> RateLimitRule:

        rule = await self.repository.get_by_id(rule_id)
        if rule is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rule not found",
            )

        return rule

    async def update(
        self,
        rule_id: UUID,
        payload: RuleUpdateRequest,
    ) -> RateLimitRule:

        rule = await self.get(rule_id)
        updates = payload.model_dump(
            exclude_unset=True
        )
        if "policy_id" in updates:
            policy = await self.policy_repository.get_by_id(
                updates["policy_id"]
            )
            if policy is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Policy does not exist",
                )
            if not policy.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot assign disabled policy",
                )

        for field,value in updates.items():
            setattr(rule,field,value)

        await self.session.commit()

        return rule

    async def set_enabled(
        self,
        rule_id: UUID,
        is_active: bool,
    ) -> RateLimitRule:

        rule = await self.get(rule_id)
        rule.is_active = is_active
        await self.session.commit()

        return rule 