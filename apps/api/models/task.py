import datetime
import uuid

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    text,
)
from sqlalchemy.dialects.postgresql import (
    UUID,
    JSONB,
    ARRAY,
)
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from shared.db.base import Base

from enum import Enum


class TaskStatus(str, Enum):

    WAITING = "waiting"

    READY = "ready"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"

    EXPANDING = "expanding"


class Task(Base):
    __tablename__ = "tasks"

    # =====================================================
    # IDENTITY
    # =====================================================

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )

    batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("batches.id"),
        nullable=False,
        index=True
    )

    batch_chapter_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("batch_chapters.id"),
        nullable=True,
        index=True
    )

    chapter_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chapters.id"),
        nullable=True,
        index=True
    )

    chapter_number: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    # =====================================================
    # TASK INFO
    # =====================================================

    task_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True
    )

    task_stage: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    task_group: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        index=True
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    # =====================================================
    # EXECUTION
    # =====================================================
    
    status: Mapped[str] = mapped_column(
        String,
        default=TaskStatus.WAITING.value,
        nullable=False,
        index=True
    )

    remaining_dependencies: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    max_retries: Mapped[int] = mapped_column(
        Integer,
        default=3
    )

    # =====================================================
    # WORKER
    # =====================================================

    worker_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        index=True
    )

    claimed_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    started_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    lease_expires_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True
    )

    # =====================================================
    # PAYLOAD
    # =====================================================

    payload: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        default=dict
    )

    result: Mapped[dict | None] = mapped_column(
        MutableDict.as_mutable(JSONB),
        nullable=True
    )

    output_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    manifest_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # =====================================================
    # RESOURCE
    # =====================================================

    required_capabilities: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list
    )

    resource_requirements: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB),
        default=dict
    )

    resource_metrics: Mapped[dict | None] = mapped_column(
        MutableDict.as_mutable(JSONB),
        nullable=True
    )

    dynamic_cost: Mapped[float | None] = mapped_column(
        nullable=True
    )

    estimated_duration: Mapped[int | None] = mapped_column(
        nullable=True
    )

    # =====================================================
    # ERROR
    # =====================================================

    error_message: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # =====================================================
    # TIMESTAMPS
    # =====================================================

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=datetime.datetime.utcnow
    )

    completed_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    failed_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    batch = relationship(
        "Batch",
        back_populates="tasks"
    )

    batch_chapter = relationship(
        "BatchChapter",
        back_populates="tasks"
    )

    chapter = relationship(
        "Chapter",
        back_populates="tasks"
    )

    parent_dependencies = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.child_task_id",
        back_populates="child_task",
        cascade="all, delete-orphan"
    )

    child_dependencies = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.parent_task_id",
        back_populates="parent_task",
        cascade="all, delete-orphan"
    )