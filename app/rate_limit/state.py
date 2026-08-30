from uuid import UUID

def build_fixed_window_key(
    *,
    rule_id: UUID,
    identity_key: str,
    window_number: int,
) -> str:

    return (
        "rl:state:fw:"
        f"{rule_id}"
        f"{identity_key}"
        f"{window_number}"
    )
