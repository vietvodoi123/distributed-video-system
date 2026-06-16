import uuid

from sqlalchemy import (
    String,
    Boolean,
    ForeignKey
)
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import (
    UUID
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from shared.db.base import Base


class Story(Base):
    __tablename__ = "stories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )

    slug: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    original_title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    ai_title: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    genre: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    tags: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    thumbnail_hook: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    background_image_url: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String,
        default="draft"
    )

    ai_profiles = relationship(
        "StoryAIProfile",
        back_populates="story",
        cascade="all, delete-orphan"
    )

    story_sources = relationship(
        "StorySource",
        back_populates="story"
    )

    chapters = relationship(
        "Chapter",
        back_populates="story"
    )

    batches = relationship(
        "Batch",
        back_populates="story"
    )

    channel_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("channels.id"),
        nullable=False
    )

    channel = relationship(
        "Channel",
        back_populates="stories"
    )