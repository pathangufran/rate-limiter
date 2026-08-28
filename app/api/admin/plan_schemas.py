from uuid import UUID
from pydantic import BaseModel,Field

class PlanCreateRequest(BaseModel):
    name: str = Field(min_length=1,max_length=100,)
    description: str | None = Field(
        default=None,
        max_length=500,
    )

class PlanUpdateRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=500,
    )
    is_active: bool | None = None

class PlanResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    is_active: bool

    model_config = {
        "from_attributes": True
    }