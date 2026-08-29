from uuid import UUID
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.admin.policy_schemas import (
    PolicyCreateRequest,
    PolicyUpdateRequest,
)
from app.models.rate_limit_policy import (
    RateLimitPolicy
)
from app.repositories.policy_repository import (
    PolicyRepository
)

class PolicyService:

    def __init__(self,session: AsyncSession,):
        self.session = session
        self.repository = PolicyRepository(session)

    async def create(
        self,
        payload: PolicyCreateRequest,
    ) -> RateLimitPolicy:

        policy = RateLimitPolicy(
            name=payload.name,
            description=payload.description,
            algorithm=payload.algorithm.value,
            request_limit=payload.request_limit,
            window_seconds=payload.window_seconds,
            burst_capacity=payload.burst_capacity,
            refill_rate=payload.refill_rate,   
        )

        await self.repository.create(policy)
        await self.session.commit()

        return policy

    async def get(
        self,
        policy_id: UUID
    ) -> RateLimitPolicy:

        policy = await self.repository.get_by_id(policy_id)

        if policy is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Policy not found",
            )

        return policy

    async def update(
        self,
        policy_id: UUID,
        payload: PolicyUpdateRequest,
    ) -> RateLimitPolicy:

        policy = await self.get(policy_id)
        updates = payload.model_dump(
            exclude_unset=True
        )
        for field,value in updates.items():
            setattr(policy,field,value)

        await self.session.commit()

        return policy

    async def set_enabled(
        self,
        policy_id: UUID,
        is_active: bool,
    ) -> RateLimitPolicy:

        policy = await self.get(policy_id)
        policy.is_active = is_active
        await self.session.commit()

        return policy