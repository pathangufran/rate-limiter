from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.plan import Plan

class PlanRepository:

    def __init__(self,session: AsyncSession):
        self.session = session

    async def create_plan(
        self,plan: Plan,
    ) -> Plan:

        self.session.add(plan)
        await self.session.flush()

        return plan

    async def get_by_id(
        self,plan_id: UUID,
    ) -> Plan | None:

        result = await self.session.execute(
            select(Plan).where(
                Plan.id == plan_id
            )
        )

        return result.scalar_one_or_none()

    async def list(self,) -> list[Plan]:

        result = await self.session.execute(
            select(Plan)
            .order_by(Plan.created_at().desc())
        )

        return list(result.scalars().all())