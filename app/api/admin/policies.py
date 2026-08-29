from uuid import UUID
from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.admin.policy_schemas import (
    PolicyCreateRequest,
    PolicyResponse,
    PolicyUpdateRequest,
)
from app.api.dependencies import CurrentUser,require_roles
from app.db.session import get_db
from app.services.policy_service import PolicyService

router = APIRouter(
    prefix="/api/v1/admin/policies",
    tags=["Rate Limit Policies"],
)

@router.post(
    "",
    response_model=PolicyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_policy(
    payload: PolicyCreateRequest,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    return await service.create(payload)

@router.get(
    "",
    response_model=list[PolicyResponse],
)
async def list_policies(
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    return await service.repository.list()

@router.get(
    "/{policy_id}",
    response_model=PolicyResponse,
)
async def get_policy(
    policy_id: UUID,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    return await service.get(policy_id)

@router.patch(
    "/{policy_id}",
    response_model=PolicyResponse,
)
async def update_policy(
    policy_id: UUID,
    payload: PolicyUpdateRequest,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    return await service.update(
        policy_id,
        payload,
    )

@router.post(
    "/{policy_id}/enable",
    response_model=PolicyResponse,
)
async def enable_policy(
    policy_id: UUID,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    return await service.set_enabled(
        policy_id,
        True,
    )

@router.post(
    "/{policy_id}/disable",
    response_model=PolicyResponse,
)
async def disable_policy(
    policy_id: UUID,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN", "SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    return await service.set_enabled(
        policy_id,
        False,
    )