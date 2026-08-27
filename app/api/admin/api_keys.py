from uuid import UUID
from fastapi import APIRouter,Depends,status,HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.admin.schemas import (
    APIKeyCreateRequest,
    APIKeyCreateResponse,
    APIKeyResponse,
)
from app.api.dependencies import CurrentUser,require_roles
from app.db.session import get_db
from app.redis.client import get_redis
from app.repositories.api_key_repository import (
    APIKeyRepository
)
from app.services.api_key_service import APIKeyService

router = APIRouter(
    prefix="/api/v1/admin/api-keys",
    tags=["API Keys"],
)

@router.post(
    "",
    response_model=APIKeyCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_api_key(
    payload: APIKeyCreateResponse,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    service = APIKeyService(
        session=session,
        redis=redis,
    )
    api_key,raw_key = await service.create(
        tenant_id=payload.tenant_id,
        name=payload.name,
        user_id=payload.user_id,
        expires_at=payload.expires_at,
    )

    await session.commit()

    return APIKeyCreateResponse(
        id=api_key.id,
        name=api_key.name,
        key=raw_key,
        prefix=api_key.prefix,
        tenant_id=api_key.tenant_id,
        user_id=api_key.user_id,
        expires_at=api_key.expires_at,
    )

@router.get(
    "",
    response_model=list[APIKeyResponse],
)
async def list_api_keys(
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    repository = APIKeyRepository(session)
    api_keys = await repository.list_for_tenant(
        current_user.tenant_id
    )

    return api_keys

@router.get(
    "/{api_key_id}",
    response_model=APIKeyResponse,
)
async def get_api_key(
    api_key_id: UUID,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    repository = APIKeyRepository(session)
    api_key = await repository.get_by_id(
        api_key_id
    )
    if (
        api_key is None
        or api_key.tenant_id != current_user.tenant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )

    return api_key

@router.post(
    "/{api_key_id}/revoke",
    response_model=APIKeyResponse,
)
async def revoke_api_key(
    api_key_id: UUID,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    repository = APIKeyRepository(session)
    api_key = await repository.get_by_id(
        api_key_id
    )
    if (
        api_key is None
        or api_key.tenant_id != current_user.tenant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )

    service = APIKeyService(
        session=session,
        redis=redis,
    )
    await service.revoke(api_key)
    await session.commit()

    return api_key