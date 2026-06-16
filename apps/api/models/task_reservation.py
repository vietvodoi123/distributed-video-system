import uuid
import datetime

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    text
)

from sqlalchemy.dialects.postgresql import (
    UUID,
    ARRAY
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from shared.db.base import Base


class TaskReservation(Base):

    __tablename__ = "task_reservations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text(
            "gen_random_uuid()"
        )
    )

    worker_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True
    )

    task_ids: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list
    )

    lease_seconds: Mapped[int] = mapped_column(
        Integer,
        default=300
    )

    expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        default="active"
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.utcnow,
        server_default=text(
            "CURRENT_TIMESTAMP"
        )
    )