from uuid import UUID

def build_identity_key(
    *,
    api_key_id: UUID | None,
    user_id: UUID | None,
    tenant_id: UUID,
    client_ip: str,
    identity_type: str,
) -> str:

    if identity_type == "api_key":
        if api_key_id is None:
            raise ValueError(
                "api_key_id is required for api_key identity"
            )

        identity_value = str(api_key_id)

    elif identity_type == "user":
        if user_id is None:
            raise ValueError(
                "user_id is required for user identity"
            )

        identity_value = str(user_id)

    elif identity_type == "tenant":
        identity_value = str(tenant_id)

    elif identity_type == "ip":
        identity_value = client_ip

    elif identity_type == "global":
        identity_value = "global"

    else:
        raise ValueError(
            f"Unsupported identity type: {identity_type}"
        )

    return (
        f"{identity_type}:{identity_value}"
    )