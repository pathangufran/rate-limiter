from datetime import datetime,timezone
from app.auth.api_key import (
    hash_api_key,
    validate_api_key_format,
)
from app.auth.exceptions import (
    InvalidAPIKeyError,
)
from app.repositories.api_key_repository import (
    APIKeyRepository,
)
from app.auth.context import AuthenticatedIdentity

class AuthenticationService:

    def __init__(
        self,
        api_key_repository: APIKeyRepository,
    ):
        self.api_key_repository = (
            api_key_repository
        )

    async def authenticate_api_key(
        self,
        api_key: str,
    ):
        if not validate_api_key_format(api_key):
            raise InvalidAPIKeyError(
                "Invalid API key"
            )

        key_hash = hash_api_key(api_key)
        api_key_record = (
            await self.api_key_repository
            .get_by_hash(key_hash)
        )

        if api_key_record is None:
            raise InvalidAPIKeyError(
                "Invalid API key"
            )

        now = datetime.now(timezone.utc)

        if (
            api_key_record.expires_at
            is not None
            and api_key_record.expires_at <= now
        ):
            raise InvalidAPIKeyError(
                "API key has expired"
            )

        return AuthenticatedIdentity(
            api_key_id=api_key_record.id,
            user_id=api_key_record.user_id,
            tenant_id=api_key_record.tenant_id,
        )