import uuid
from sqlalchemy import (
    String,
    Boolean,
    Integer
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


class Website(Base):
    __tablename__ = "websites"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default = text("gen_random_uuid()")
    )

    # identity
    code: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    base_url: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    # execution
    parser_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    render_engine: Mapped[str] = mapped_column(
        String,
        default="http"
    )

    # features
    enable_translate: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    use_proxy: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    # throttling
    rate_limit: Mapped[int] = mapped_column(
        Integer,
        default=60
    )

    request_delay: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    timeout: Mapped[int] = mapped_column(
        Integer,
        default=30
    )

    retry_limit: Mapped[int] = mapped_column(
        Integer,
        default=3
    )

    max_concurrency: Mapped[int] = mapped_column(
        Integer,
        default=3
    )

    # dynamic crawler config
    crawler_config: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb")
    )

    story_sources = relationship(
        "StorySource",
        back_populates="website"
    )