from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.admin.schemas import (
    LoginRequest,
    LoginResponse,
)
from app.db.session import get_db
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/api/v1/admin/auth",
    tags=["Admin Authentication"],
)

@router.post("/login",response_model=LoginResponse,)
async def login(
    payload: LoginRequest,
    session: AsyncSession = Depends(get_db),
):
    service = AuthService(session)
    token = await service.login(
        email=payload.email,
        password=payload.password,
    )

    return LoginResponse(
        access_token=token,
        expires_in=30 * 60,
    )