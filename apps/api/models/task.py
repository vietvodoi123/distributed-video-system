import uuid
from sqlalchemy.dialects.postgresql import (
    UUID,
    JSONB,
    ARRAY
)

from sqlalchemy.ext.mutable import MutableDict
import datetime
from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    Boolean,
    DateTime
)

from sqlalchemy import text

from sqlalchemy.dialects.postgresql import (
    UUID,
    JSONB
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from shared.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )

    # =====================================
    # RELATIONS
    # =====================================

    batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("batches.id"),
        nullable=False
    )

    batch_chapter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("batch_chapters.id"),
        nullable=True
    )

    chapter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chapters.id"),
        nullable=True
    )

    chapter_number: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
    # =====================================
    # TASK INFO
    # =====================================

    task_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    task_stage: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    task_group: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        index = True
    )
    required_capabilities: Mapped[list] = mapped_column(
        ARRAY(String),
        default=list
    )
    # =====================================
    # DAG
    # =====================================

    depends_on_task_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id"),
        nullable=True
    )
    downstream_tasks = relationship(

        "Task",

        back_populates="depends_on_task"
    )

    wait_for_task_types: Mapped[list] = mapped_column(
        ARRAY(String),
        default=list
    )
    # =====================================
    # EXECUTION
    # =====================================

    status: Mapped[str] = mapped_column(
        String,
        default="pending"
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    max_retries: Mapped[int] = mapped_column(
        Integer,
        default=3
    )

    is_blocking: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    # =====================================
    # WORKER
    # =====================================

    worker_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    lease_expires_at: Mapped[datetime.datetime | None] = mapped_column(
        nullable=True
    )

    # =====================================
    # PAYLOAD
    # =====================================

    payload: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        default=dict
    )

    result: Mapped[dict | None] = mapped_column(
        MutableDict.as_mutable(JSONB),
        nullable=True
    )

    resource_requirements: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        default=dict
    )

    resource_metrics: Mapped[dict | None] = mapped_column(
        MutableDict.as_mutable(JSONB),
        nullable=True
    )


    error_message: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # =====================================
    # OUTPUTS
    # =====================================

    output_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    manifest_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # =====================================
    # RELATIONSHIPS
    # =====================================

    batch = relationship(
        "Batch",
        back_populates="tasks"
    )

    chapter = relationship(
        "Chapter",
        back_populates="tasks"
    )

    depends_on_task = relationship(
        "Task",
        remote_side=[id],
        uselist=False
    )
    batch_chapter = relationship(
        "BatchChapter",
        back_populates="tasks"
    )
    claimed_by: Mapped[str | None] = mapped_column(
        nullable=True
    )

    claimed_at: Mapped[datetime.datetime | None] = mapped_column(
        nullable=True
    )

    started_at: Mapped[datetime.datetime | None] = mapped_column(
        nullable=True
    )

    completed_at: Mapped[datetime.datetime | None] = mapped_column(
        nullable=True
    )

    failed_at: Mapped[datetime.datetime | None] = mapped_column(
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

    updated_at: Mapped[
        datetime.datetime | None
        ] = mapped_column(

        DateTime(timezone=True),

        nullable=True,

        onupdate=datetime.datetime.utcnow
    )


    dynamic_cost: Mapped[float | None] = mapped_column(
        nullable=True
    )

    estimated_duration: Mapped[int | None] = mapped_column(
        nullable=True
    )
