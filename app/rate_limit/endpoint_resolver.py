from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.endpoint_repository import (
    EndpointRepository
)

class EndpointResolver:

    def __init__(self,session: AsyncSession):

        self.repository = EndpointRepository(session)

    async def resolve(
        self,
        *,
        method: str,
        path: str,
    ):
        endpoints = await self.repository.list()
        for endpoint in endpoints:
            if not endpoint.is_active:
                continue
            if endpoint.method != method.upper():
                continue
            if endpoint.path == path:
                return endpoint

        return None