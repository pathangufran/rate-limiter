from uuid import UUID
from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.admin.rule_schemas import (
    RuleCreateRequest,
    RuleResponse,
    RuleUpdateRequest,
)
from app.api.dependencies import CurrentUser,require_roles
from app.db.session import get_db
from app.services.rule_service import RuleService

router = APIRouter(
    prefix="/api/v1/admin/rules",
    tags=["Rate Limit Rules"],
)

@router.post(
    "",
    response_model=RuleResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_rule(
    payload: RuleCreateRequest,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    service = RuleService(session)

    return await service.create(payload)

@router.get(
    "",
    response_model=list[RuleResponse],
)
async def list_rules(
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    service = RuleService(session)

    return await service.repository.list()

@router.get(
    "/{rule_id}",
    response_model=RuleResponse,
)
async def get_rule(
    rule_id: UUID,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    service = RuleService(session)

    return await service.get(rule_id)

@router.patch(
    "/{rule_id}",
    response_model=RuleResponse,
)
async def update_rule(
    rule_id: UUID,
    payload: RuleUpdateRequest,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    service = RuleService(session)

    return await service.updatee(
        rule_id,
        payload,
    )

@router.post(
    "/{rule_id}/enable",
    response_model=RuleResponse,
)
async def enable_rule(
    rule_id: UUID,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    service = RuleService(session)

    return await service.set_enabled(
        rule_id,
        True,
    )

@router.post(
    "/{rule_id}/disable",
    response_model=RuleResponse,
)
async def enable_rule(
    rule_id: UUID,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    service = RuleService(session)

    return await service.set_enabled(
        rule_id,
        False,
    )