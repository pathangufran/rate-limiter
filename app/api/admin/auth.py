from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class CurrentUser:
    user_id: UUID
    tenant_id: UUID
    role: str

@dataclass(frozen=True)
class APIKeyIdentity:
    api_key_id: UUID
    tenant_id: UUID
    user_id: UUID | None
    expires_at: datetime | None