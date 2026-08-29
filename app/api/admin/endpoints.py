from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter,Depends,HTTPException,status
from app.api.admin.endpoint_schemas import (
    EndpointCreateRequest,
    EndpointResponse,
    EndpointUpdateRequest,
)
from app.api.dependencies import CurrentUser,require_roles
from app.db.session import get_db
from app.models.endpoint import Endpoint
from app.repositories.endpoint_repository import (
    EndpointRepository
)

router = APIRouter(
    prefix="/api/v1/admin/endpoints",
    tags=["Endpoints"],
)

@router.post(
    "",
    response_model=EndpointResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_endpoing(
    payload : EndpointCreateRequest,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    repository = EndpointRepository(session)
    endpoint = Endpoint(
        method=payload.method,
        path=payload.path,
        name=payload.name,
    )

    await repository.create(endpoint)
    await session.commit()

    return endpoint

@router.get(
    "",
    response_model=list[EndpointResponse]
)
async def list_endpoint(
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    repository = EndpointRepository(session)

    return await repository.list()

@router.get(
    "/{endpoint_id}",
    response_model=EndpointResponse,
)
async def get_endpoint(
    endpoint_id: UUID,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    repository = EndpointRepository(session)

    endpoint = await repository.get_by_id(endpoint_id)
    if endpoint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found",
        )

    return endpoint

@router.patch(
    "/{endpoint_id}",
    response_model=EndpointResponse,
)
async def update_endpoint(
    endpoint_id: UUID,
    payload: EndpointUpdateRequest,
    current_user: CurrentUser = Depends(
        require_roles("ADMIN","SUPER_ADMIN")
    ),
    session: AsyncSession = Depends(get_db),
):
    repository = EndpointRepository(session)
    endpoint = await repository.get_by_id(endpoint_id)

    if endpoint is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found",
        )

    updates = payload.model_dump(
        exclude_unset=True
    )
    for field,value in updates.items():
        setattr(endpoint,field,value)

    await session.commit()

    return endpoint