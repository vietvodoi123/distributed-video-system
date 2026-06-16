import uuid
from sqlalchemy import text

from sqlalchemy import (
    String,
    Boolean,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import (
    UUID
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from shared.db.base import Base


class StoryAIProfile(Base):
    __tablename__ = "story_ai_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()")
    )

    story_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("stories.id"),
        nullable=False
    )

    # identity
    profile_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # prompting
    positive_prompt: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    negative_prompt: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    thumbnail_hook_template: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # narration
    narration_style: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    tts_voice: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    tts_model: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # image / visual
    image_style: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # llm
    llm_model: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # flags
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    # relationships
    story = relationship(
        "Story",
        back_populates="ai_profiles"
    )