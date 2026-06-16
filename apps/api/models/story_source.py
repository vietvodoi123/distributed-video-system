import uuid

from sqlalchemy import (
    String,
    Boolean,
    Integer,
    ForeignKey
)

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
from sqlalchemy import text


class StorySource(Base):
    __tablename__ = "story_sources"

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

    website_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("websites.id"),
        nullable=False
    )

    # source identity
    source_url: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    source_story_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # chapter tracking
    latest_chapter: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    total_chapters: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    # crawler state
    crawl_status: Mapped[str] = mapped_column(
        String,
        default="pending"
    )

    last_crawled_at: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    last_chapter_crawled_at: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    last_successful_crawl_at: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # flags
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    source_config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict
    )

    # relationships
    story = relationship(
        "Story",
        back_populates="story_sources"
    )

    website = relationship(
        "Website",
        back_populates="story_sources"
    )

