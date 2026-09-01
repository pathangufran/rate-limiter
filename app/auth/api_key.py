import re
import hashlib

def hash_api_key(
    api_key: str,
) -> str:

    return hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()

API_KEY_PATTERN = re.compile(
    r"^rl_(live|test)_[A-Za-z0-9_-]{16,}$"
)

def validate_api_key_format(
    api_key: str,
) -> bool:

    return bool(
        API_KEY_PATTERN.fullmatch(
            api_key
        )
    )

API_KEY_HEADER = "X-API-Key"