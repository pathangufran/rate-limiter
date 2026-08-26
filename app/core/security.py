import jwt
from typing import Any
from pwdlib import PasswordHash
from datetime import datetime,timedelta,timezone
from app.core.config import settings

password_hasher = PasswordHash.recommended()

class SecurityError(Exception):
    """Base exception for security-related failures."""

class InvalidTokenError(SecurityError):
    """Raised when a JWT is invalid or expired."""

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(password: str,
    password_hash: str,) -> bool:

    return password_hasher.verify(
        password,
        password_hash,
    )

def create_access_token(
    *,
    user_id: str,
    tenant_id: str,
    role: str,
) -> str:
    now = datetime.now(timezone.utc)

    payload: dict[str,Any] = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "role": role,
        "type": "access",
        "iat": now,
        "exp": now
        + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        ),
    }
    
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

def decode_access_token(token: str) -> dict[str,Any]:
    try:
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

    except jwt.PyJWTError as exc:
        raise InvalidTokenError(
            "Invalid or expired access token"
        ) from exc