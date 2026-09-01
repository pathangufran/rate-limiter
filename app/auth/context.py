from uuid import UUID
from dataclasses import dataclass

@dataclass(frozen=True)
class AuthenticatedIdentity:
    api_key_id: UUID
    user_id: UUID
    tenant_id: UUID