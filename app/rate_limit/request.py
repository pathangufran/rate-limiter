from fastapi import Request

API_KEY_HEADER = "X-API-Key"

def get_api_key(request: Request,) -> str | None:

    return request.headers.get(API_KEY_HEADER)