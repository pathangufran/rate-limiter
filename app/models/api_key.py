import uuid
from datetime import datetime
from sqlalchemy import (
    Boolean,String,ForeignKey,DateTime,Index,
)
from sqlalchemy.orm import (
    Mapped,mapped_column,relationship,
)
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    key_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    prefix: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default="now()",
    )
    tenant = relationship(
        "Tenant",
        back_populates="api_keys",
    )
    user = relationship(
        "User",
        back_populates="api_keys",
    )

    __table_args__ = (
        Index(
            "ix_api_keys_tenant_id",
            "tenant_id",
        ),
        Index(
            "ix_api_keys_user_id",
            "user_id",
        ),
        Index(
            "ix_api_keys_active",
            "is_active",
        ),
    )