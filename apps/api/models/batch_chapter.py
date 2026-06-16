import uuid

from sqlalchemy import (
    ForeignKey,
    Integer,
    String
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


class BatchChapter(Base):
    __tablename__ = "batch_chapters"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )

    # relations
    batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("batches.id"),
        nullable=False
    )

    chapter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chapters.id"),
        nullable=False
    )

    # deterministic ordering
    order_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # orchestration
    status: Mapped[str] = mapped_column(
        String,
        default="pending"
    )

    # outputs
    chapter_video_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    subtitle_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    audio_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    manifest_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # metadata
    render_metadata: Mapped[dict] = mapped_column(
        JSONB,
        default=dict
    )

    # relationships
    batch = relationship(
        "Batch",
        back_populates="batch_chapters"
    )

    chapter = relationship(
        "Chapter"
    )

    tasks = relationship(
        "Task",
        back_populates="batch_chapter"
    )