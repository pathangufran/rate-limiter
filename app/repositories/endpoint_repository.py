from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.endpoint import Endpoint

class EndpointRepository:

    def __init__(self,session: AsyncSession):
        self.session = session

    async def create(
        self,endpoint: Endpoint,
    ) -> Endpoint:

        self.session.add(endpoint)
        await self.session.flush()

        return endpoint

    async def get_by_id(
        self,endpoint_id: UUID,
    ) -> Endpoint | None:

        result = await self.session.execute(
            select(Endpoint).where(
                Endpoint.id == endpoint_id
            )
        )

        return result.scalar_one_or_none()

    async def list(self,) -> list[Endpoint]:

        result = await self.session.execute(
            select(Endpoint)
            .order_by(Endpoint.created_at().desc())
        )

        return list(result.scalars().all())