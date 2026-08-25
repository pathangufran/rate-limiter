import uuid
from decimal import Decimal
from sqlalchemy import Boolean,Integer,Numeric,String,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
from app.models.base import TimestampMixin

class RateLimitPolicy(TimestampMixin,Base):
    __tablename__ = "rate_limit_policies"

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    algorithm: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    request_limit: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    window_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    burst_capacity: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    refill_rate: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 4),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    rules = relationship(
        "RateLimitRule",
        back_populates="policy",
    )
