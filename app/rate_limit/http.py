from fastapi.responses import JSONResponse
from app.rate_limit.headers import (
    RATE_LIMIT_LIMIT,
    RATE_LIMIT_REMAINING,
    RATE_LIMIT_RESET,
    RETRY_AFTER,
)

def build_rate_limit_headers(
    *,
    limit: int,
    remaining: int,
    reset_after: int,
    retry_after: int | None = None,
) -> dict[str,str]:

    headers = {
        RATE_LIMIT_LIMIT: str(limit),
        RATE_LIMIT_REMAINING: str(
            max(0,remaining)
        ),
        RATE_LIMIT_RESET: str(
            max(0,reset_after)
        ),
    }

    if retry_after is not None:

        headers[RETRY_AFTER] = str(
            max(0,retry_after)
        )

    return headers

def build_rate_limit_response(
    *,
    rule_id,
    result,
) -> JSONResponse:

    headers = build_rate_limit_headers(
        limit=result.limit,
        remaining=result.remaining,
        reset_after=result.reset_after,
        retry_after=result.retry_after,
    )

    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded",
            "error": "rate_limit_exceeded",
            "rule_id": (
                str(rule_id)
                if rule_id is not None
                else None
            ),
        },
        headers=headers,
    )