import hashlib
import secrets

API_KEY_PREFIX = "rl_live_"

def generate_api_key() -> tuple[
    str,
    str,
    str,
]:
    secret = secrets.token_urlsafe(32)
    raw_key = (
        f"{API_KEY_PREFIX}"
        f"{secret}"
    )

    key_hash = hashlib.sha256(
        raw_key.encode("utf-8")
    ).hexdigest()

    key_prefix = raw_key[:12]

    return (
        raw_key,
        key_prefix,
        key_hash,
    )