from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.models import (  # noqa: E402,F401
    APIKey,
    AuditLog,
    Endpoint,
    Plan,
    RateLimitPolicy,
    RateLimitRule,
    Tenant,
    user,
)