from app.rate_limit.context import RateLimitContext

class IdentityResolver:

    def resolve(
        self,
        *,
        context: RateLimitContext,
        identity_type: str,
        endpoint: str | None = None,
    ) -> str:

        if identity_type == "GLOBAL":
            return "global"
        
        if identity_type == "TENANT":
            if context.identity.tenant_id is None:
                raise ValueError(
                    "tenant_id is required"
                )
            return (
                f"tenant:"
                f"{context.identity.tenant_id}"
            )
        
        if identity_type == "USER":
            if context.identity.user_id is None:
                raise ValueError(
                    "user_id is required"
                )
            return (
                f"user:"
                f"{context.identity.user_id}"
            )
        
        if identity_type == "API_KEY":
            if context.identity.api_key_id is None:
                raise ValueError(
                    "api_key_id is required"
                )
            return (
                f"api_key:"
                f"{context.identity.api_key_id}"
            )
        
        if identity_type == "IP":
            if not context.identity.client_ip:
                raise ValueError(
                    "client_ip is required"
                )
            return (
                f"ip:"
                f"{context.identity.client_ip}"
            )

        if identity_type == "ENDPOINT":
            if not endpoint:
                raise ValueError(
                    "endpoint is required"
                )
            return (
                f"endpoint:"
                f"{endpoint}"
            )
        
        raise ValueError(
            f"Unsupported identity type: {identity_type}"
        )