from sqlalchemy import (
    String,
)

from sqlalchemy.orm import (
    mapped_column,
    relationship
)
import uuid

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID

from shared.db.base import Base

class Channel(Base):

    __tablename__ = "channels"

    id = mapped_column(
        UUID(as_uuid=True),

        primary_key=True,

        default=uuid.uuid4,

        server_default=text(
            "gen_random_uuid()"
        )
    )

    youtube_channel_id = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    mc_name = mapped_column(
        String,
        nullable=False
    )

    mc_path = mapped_column(
        String,
        nullable=False
    )

    stories = relationship(
        "Story",
        back_populates="channel"
    )