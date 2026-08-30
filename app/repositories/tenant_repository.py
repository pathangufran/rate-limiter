from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tenant import Tenant

class TenantRepository:

    def __init__(self,session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        tenant_id: UUID,
    ) -> Tenant | None:

        result = await self.session.execute(
            select(Tenant)
            .options(
                selectinload(Tenant.plan)
            )
            .where(
                Tenant.id == tenant_id
            )
        )

        return result.scalar_one_or_none()