import uuid
import datetime

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    text
)

from sqlalchemy.dialects.postgresql import (
    UUID,
    ARRAY,
    JSONB
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from shared.db.base import Base


class Worker(Base):

    __tablename__ = "workers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text(
            "gen_random_uuid()"
        )
    )

    # =====================================
    # IDENTITY
    # =====================================

    worker_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    worker_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # =====================================
    # CAPABILITIES
    # =====================================

    capabilities: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list
    )

    # =====================================
    # EXECUTION
    # =====================================

    max_concurrency: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    free_slots: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    # =====================================
    # DEVICE STATE
    # =====================================

    battery: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    temperature: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    is_charging: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True
    )

    # =====================================
    # NETWORK
    # =====================================

    tailscale_ip: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # =====================================
    # STATUS
    # =====================================

    status: Mapped[str] = mapped_column(
        String,
        default="online"
    )

    last_heartbeat: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.utcnow
    )

    # =====================================
    # EXTRA
    # =====================================

    extra_data: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.utcnow,
        server_default=text(
            "CURRENT_TIMESTAMP"
        )
    )

    resource_weights: Mapped[dict] = mapped_column(
        JSONB,
        default=dict
    )

    resource_capacity: Mapped[dict] = mapped_column(
        JSONB,
        default=dict
    )

    current_load: Mapped[dict] = mapped_column(
        JSONB,
        default=dict
    )

    current_dynamic_cost: Mapped[float | None] = mapped_column(
        nullable=True
    )

    max_dynamic_cost: Mapped[float | None] = mapped_column(
        nullable=True
    )