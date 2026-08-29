from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.admin.plan_schemas import (
    PlanCreateRequest,
    PlanResponse,
    PlanUpdateRequest,
)
from app.api.dependencies import CurrentUser,require_roles
from app.db.session import get_db
from app.models.plan import Plan
from app.repositories.plan_repository import (
    PlanRepository
)

router = APIRouter(
    prefix="/api/v1/admin/plans",
    tags=["Plans"],
)

@router.post(
    "",
    response_model=PlanResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_plan(
    payload: PlanCreateRequest,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    repository = PlanRepository(session)
    plan = Plan(
        name=payload.name,
        description=payload.description,
    )

    await repository.create(plan)
    await session.commit()

    return plan

@router.get(
    "",
    response_model=list[PlanResponse],
)
async def list_plans(
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    repository = PlanRepository(session)

    return await repository.list()

@router.get(
    "/{plan_id}",
    response_model=PlanResponse,
)
async def get_plan(
    plan_id: UUID,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    repository = PlanRepository(session)
    plan = await repository.get_by_id(plan_id)

    if plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )

    return plan

@router.patch(
    "/{plan_id}",
    response_model=PlanResponse,
)
async def update_plan(
    plan_id: UUID,
    payload: PlanUpdateRequest,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    repository = PlanRepository(session)
    plan = await repository.get_by_id(plan_id)

    if plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )

    updates = payload.model_dump(
        exclude_unset=True
    )

    for field,value in updates.items():
        setattr(plan,field,value)

    await session.commit()

    return plan