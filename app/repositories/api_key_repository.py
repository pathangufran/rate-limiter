from datetime import datetime,timezone
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.api_key import APIKey

class APIKeyRepository:

    def __init__(self,session: AsyncSession):
        self.session = session

    async def get_by_id(self,api_key_id:UUID
    ) -> APIKey | None:

        result = await self.session.execute(
            select(APIKey).where(
                APIKey.id == api_key_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_hash(self,key_hash: str,
    ) -> APIKey | None:

        result = await self.session.execute(
            select(APIKey).where(
                APIKey.key_hash == key_hash
            )
        )

        return result.scalar_one_or_none()

    async def create(self,api_key: APIKey) -> APIKey:

        self.session.add(api_key)
        await self.session.flush()

        return api_key

    async def list_for_tenant(self,
    tenant_id: UUID) -> list[APIKey]:

        result = await self.session.execute(
            select(APIKey)
            .where(APIKey.tenant_id == tenant_id)
            .order_by(APIKey.created_at.desc())
        )

        return list(result.scalars().all())

    async def revoke(self,api_key: APIKey,) -> APIKey:

        api_key.is_active = False
        api_key.revoked_at = datetime.now(timezone.utc)

        await self.session.flush()

        return api_key