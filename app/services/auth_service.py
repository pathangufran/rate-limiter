from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import (
    create_access_token,
    verify_password,
)
from app.repositories.user_repository import UserRepository

class AuthService:

    def __init__(self,session: AsyncSession):
        self.user_repository = UserRepository(session)

    async def login(self,*,email: str,password:
    str,) -> str:

        user = self.user_repository.get_by_email(
            email
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        if not verify_password(password,user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        return create_access_token(
            user_id=str(user.id),
            tenant_id=str(user.tenant_id),
            role=user.role,
        )