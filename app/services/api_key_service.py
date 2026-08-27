import json
from datetime import datetime,timezone
from uuid import UUID
from fastapi import HTTPException,status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.api_keys import (
    generate_api_key,
    hash_api_key
)
from app.core.auth import APIKeyIdentity
from app.core.config import settings
from app.models.api_key import APIKey
from app.repositories.api_key_repository import (
    APIKeyRepository
)

class APIKeyService:

    CACHE_PREFIX = "auth:apikey:"

    def __init__(self,session: AsyncSession,
    redis: Redis,):
        self.repository = APIKeyRepository(session)
        self.redis = redis

    def _cache_key(self,key_hash: str) -> str:
        return f"{self.CACHE_PREFIX}{key_hash}"

    @staticmethod
    def _serializer_identity(api_key: APIKey,) -> str:

        data = {
            "api_key_id": str(api_key.id),
            "tenant_id": str(api_key.tenant_id),
            "user_id": (
                str(api_key.user_id)
                if api_key.user_id
                else None
            ),
            "expires_at": (
                api_key.expires_at.isoformat()
                if api_key.expires_at
                else None
            ),
        }

        return json.dumps(data)

    @staticmethod
    def _deserialize_identity(data: str,) -> APIKeyIdentity:

        payload = json.loads(data)
        expires_at = payload.get("expires_at")

        return APIKeyIdentity(
            api_key_id=UUID(payload["api_key_id"]),
            tenant_id=UUID(payload["tenant_id"]),
            user_id=(
                UUID(payload["user_id"])
                if payload.get("user_id")
                else None
            ),
            expires_at=(
                datetime.fromisoformat(expires_at)
                if expires_at
                else None
            ),
        )

    async def create(
        self,*,tenant_id: UUID,name: str,
        user_id: UUID | None = None,
        expires_at: datetime | None = None,
    ) -> tuple[APIKey, str]:

        raw_key,prefix,key_hash = generate_api_key()

        api_key = APIKey(
            tenant_id=tenant_id,
            user_id=user_id,
            name=name,
            key_hash=key_hash,
            prefix=prefix,
            expires_at=expires_at,
        )
        await self.repository.create(api_key)

        return api_key,raw_key

    async def authenticate(self,raw_key: str,) -> APIKeyIdentity:

        key_hash = hash_api_key(raw_key)
        cache_key = self._cache_key(key_hash)
        cached = self.redis.get(cache_key)

        if cached:
            identity = self._deserialize_identity(cached)
            if (
                identity.expires_at is not None
                and identity.expires_at
                <= datetime.now(timezone.utc)
            ):
                await self.redis.delete(cache_key)

        else:
            return identity

        api_key = await self.repository.get_by_hash(
            key_hash
        )
        if api_key is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )

        now = datetime.now(timezone.utc)
        if not api_key.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )
        if api_key.revoked_at is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )
        if (
            api_key.expires_at is not None
            and api_key.expires_at <= now
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key expired",
            )

        identity = APIKeyIdentity(
            api_key_id=api_key.id,
            tenant_id=api_key.tenant_id,
            user_id=api_key.user_id,
            expires_at=api_key.expires_at,
        )
        await self.redis.set(
            cache_key,
            self._serializer_identity(api_key),
            ex=settings.api_key_cache_ttl_seconds,
        )

        return identity

    async def revoke(self,api_key: APIKey,) -> APIKey:

        revoked = await self.repository.revoke(api_key)
        await self.redis.delete(
            self._cache_key(api_key.key_hash)
        )

        return revoked
