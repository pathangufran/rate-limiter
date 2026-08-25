import uuid
from sqlalchemy import Boolean,String,UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base
from app.models.base import TimestampMixin

class Endpoint(TimestampMixin,Base):
    __tablename__ = "endpoints"

    __table_args__ = (
        UniqueConstraint(
            "method",
            "path",
            name="uq_endpoint_method_path",
        ),
    )

    method: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    rules = relationship(
        "RateLimitRule",
        back_populates="endpoint",
    )
