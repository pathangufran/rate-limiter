from uuid import UUID
from fastapi import Depends,HTTPException,status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import APIKeyIdentity,CurrentUser
from app.core.security import (
    InvalidTokenError,
    decode_access_token,
)
from app.db.session import get_db
from app.redis.client import get_redis
from app.services.api_key_service import APIKeyService

bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None
    = Depends(bearer_scheme),
) -> CurrentUser:

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )

    try:
        payload = decode_access_token(
            credentials.credentials
        )

    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        ) from exc

    try:
        user_id = UUID(payload["sub"])
        tenant_id = UUID(payload["tenant_id"])
        role = payload["role"]

    except (KeyError,ValueError,TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        ) from exc

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    return CurrentUser(
        user_id=user_id,
        tenant_id=tenant_id,
        role=role,
    )

def require_roles(*allowed_roles: str):

    async def dependency(
        current_user: CurrentUser = Depends(
            get_current_user
        ),
    ) -> CurrentUser:

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return dependency

async def get_api_key_identity(
    credentials: HTTPAuthorizationCredentials | None
    = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> APIKeyIdentity:

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
        )
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )

    api_key = credentials.credentials
    if not api_key.startswith("rl_live_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    service = APIKeyService(
        session=session,
        redis=redis,
    )

    return await service.authenticate(api_key)