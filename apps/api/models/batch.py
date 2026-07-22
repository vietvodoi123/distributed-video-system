import uuid
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy import (
    String,
    ForeignKey,
    Integer
)
from sqlalchemy import UniqueConstraint
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


class Batch(Base):
    __tablename__ = "batches"
    __table_args__ = (

        UniqueConstraint(

            "story_id",

            "start_chapter",

            "end_chapter",

            name="uq_story_batch_range"
        ),

    )
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )

    # relations
    story_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("stories.id"),
        nullable=False
    )

    story_source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("story_sources.id"),
        nullable=False
    )

    # identity
    batch_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # range
    start_chapter: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    end_chapter: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # orchestration
    total_chapters: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    completed_chapters: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    failed_chapters: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    # outputs
    manifest_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    output_dir: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    final_video_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )
    cleanup_status = mapped_column(
        String,
        nullable=False,
        default="none"
    )
    # config
    batch_config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict
    )

    # state
    status: Mapped[str] = mapped_column(
        String,
        default="pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )
    # relationships
    story = relationship(
        "Story",
        back_populates="batches"
    )

    story_source = relationship(
        "StorySource"
    )

    batch_chapters = relationship(
        "BatchChapter",
        back_populates="batch",
        cascade="all, delete-orphan"
    )

    tasks = relationship(
        "Task",
        back_populates="batch"
    )
