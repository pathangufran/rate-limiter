import hashlib
import secrets
from app.core.config import settings

def generate_api_key() -> tuple[str,str,str]:
    secret = secrets.token_urlsafe(32)
    raw_key = f"{settings.api_key_prefix}{secret}"
    prefix = raw_key[:16]

    key_hash = hashlib.sha256(
        raw_key.encode("utf-8")
    ).hexdigest()

    return raw_key,prefix,key_hash

def hash_api_key(raw_key: str) -> str:
    return hashlib.sha256(
        raw_key.encode("uft-8")
    ).hexdigest()

