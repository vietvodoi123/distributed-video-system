import uuid
import datetime
from enum import Enum

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index,
    text,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from shared.db.base import Base


class DependencyType(str, Enum):

    SUCCESS = "success"

    COMPLETED = "completed"

    FAILED = "failed"

    OPTIONAL = "optional"


class TaskDependency(Base):
    __tablename__ = "task_dependencies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )

    # =====================================================
    # GRAPH
    # =====================================================

    parent_task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "tasks.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    child_task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "tasks.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    dependency_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=DependencyType.SUCCESS.value
    )

    # =====================================================
    # TIMESTAMP
    # =====================================================

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP")
    )

    # =====================================================
    # RELATIONSHIP
    # =====================================================

    parent_task = relationship(
        "Task",
        foreign_keys=[parent_task_id],
        back_populates="child_dependencies"
    )

    child_task = relationship(
        "Task",
        foreign_keys=[child_task_id],
        back_populates="parent_dependencies"
    )

    # =====================================================
    # CONSTRAINTS
    # =====================================================

    __table_args__ = (

        UniqueConstraint(
            "parent_task_id",
            "child_task_id",
            name="uq_task_dependency"
        ),

        Index(
            "idx_dependency_parent",
            "parent_task_id"
        ),

        Index(
            "idx_dependency_child",
            "child_task_id"
        ),
    )