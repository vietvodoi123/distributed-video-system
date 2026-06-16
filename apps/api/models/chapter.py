import uuid
from sqlalchemy import text
from sqlalchemy import (
    String,
    Integer,
    ForeignKey
)
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import (
    UUID
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from shared.db.base import Base


class Chapter(Base):
    __tablename__ = "chapters"
    __table_args__ = (

        UniqueConstraint(
            "story_source_id",
            "chapter_number",
            name="uq_story_source_chapter"
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
    chapter_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    chapter_code: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    source_chapter_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # titles
    original_title: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    translated_title: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # source
    source_url: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # text pipeline
    raw_text: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    translated_text: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    final_script: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # overall status
    status: Mapped[str] = mapped_column(
        String,
        default="pending"
    )

    # pipeline statuses
    translation_status: Mapped[str] = mapped_column(
        String,
        default="pending"
    )

    tts_status: Mapped[str] = mapped_column(
        String,
        default="pending"
    )

    render_status: Mapped[str] = mapped_column(
        String,
        default="pending"
    )

    # video info
    video_duration: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    # publishing
    published_at: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # relationships
    story = relationship(
        "Story",
        back_populates="chapters"
    )

    story_source = relationship(
        "StorySource"
    )

    tasks = relationship(
        "Task",
        back_populates="chapter"
    )