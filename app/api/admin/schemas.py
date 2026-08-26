from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,ConfigDict,EmailStr,Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class APIKeyCreateRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=150,
    )
    tenant_id: UUID
    user_id: UUID | None = None
    expires_at: datetime | None = None

class APIKeyCreateResponse(BaseModel):
    id: UUID
    name: str
    key: str
    prefix: str
    tenant_id: UUID
    user_id: UUID | None
    expires_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

class APIKeyResponse(BaseModel):
    id: UUID
    name: str
    prefix: str
    tenant_id: UUID
    user_id: UUID | None
    is_active: bool
    expires_at: datetime | None
    revoked_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)