from uuid import UUID
from pydantic import BaseModel,Field,field_validator

VALID_METHODS = {
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
    "HEAD",
}

class EndpointCreateRequest(BaseModel):
    method: str
    path: str = Field(min_length=1,max_length=500,)
    name: str | None = Field(
        default=None,
        max_length=150,
    )

    @field_validator("method")
    @classmethod
    def validate_method(cls,value: str) -> str:
        value = value.upper()

        if value not in VALID_METHODS:
            raise ValueError(
                f"Unsupported HTTP method: {value}"
            )

        return value

    @field_validator("path")
    @classmethod
    def validate_path(cls,value: str) -> str:

        if not value.startswith("/"):
            raise ValueError(
                "Endpoint path must start with '/'"
            )

        return value

class EndpointUpdateRequest(BaseModel):
    method: str | None = None
    path: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
    )
    name: str | None = Field(
        default=None,
        max_length=150,
    )
    is_active: bool | None = None

class EndpointResponse(BaseModel):
    id: UUID
    method: str
    path: str
    name: str | None
    is_active: bool

    model_config = {
        "from_attributes": True
    }