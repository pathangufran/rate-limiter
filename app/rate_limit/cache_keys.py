RULE_CACHE_NAMESPACE = (
    "rate_limit:rule_generation"
)

RULE_CACHE_VERSION = "v1"

def normalize_endpoint(
    endpoint: str,
) -> str:
    """
    Normalize endpoint paths so equivalent
    paths don't create different cache keys.
    """
    if not endpoint:
        return "/"

    if endpoint != "/":
        endpoint = endpoint.rstrip("/")

    return endpoint

def normalize_method(
    method: str,
) -> str:
    """
    HTTP methods are case-insensitive for the
    purpose of our cache key.
    """

    return method.upper()

def build_rule_cache_key(
    *,
    tenant_id: int,
    generation: int,
    method: str,
    endpoint: str,
    identity_type: str,
    identity_id: str,
) -> str:

    endpoint = normalize_endpoint(
        endpoint
    )
    method = normalize_method(
        method
    )

    return (
        f"{RULE_CACHE_NAMESPACE}:"
        f"{RULE_CACHE_VERSION}:"
        f"tenant:{tenant_id}:"
        f"generation:{generation}:"
        f"method:{method}:"
        f"endpoint:{endpoint}:"
        f"identity:{identity_type}:"
        f"{identity_id}"
    )

def build_rule_generation_key(
    *,
    tenant_id: int,
) -> str:

    return (
        f"{RULE_CACHE_NAMESPACE}:"
        f"tenant:{tenant_id}"
    )