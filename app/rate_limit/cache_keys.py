def build_rule_cache_key(
    *,
    tenant_id: int,
    method: str,
    endpoint: str,
    identity_id: str,
) -> str:

    return (
        "rate_limit:rules:"
        f"tenant:{tenant_id}:"
        f"method:{method.upper()}:"
        f"endpoint:{endpoint}:"
        f"identity:{identity_id}"
    )