"""make task refs nullable

Revision ID: fe42584b72f7
Revises: b60e5acccc40
Create Date: 2026-05-24 16:03:09.731734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe42584b72f7'
down_revision: Union[str, Sequence[str], None] = 'b60e5acccc40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.alter_column(
        "tasks",
        "batch_chapter_id",
        existing_type=sa.UUID(),
        nullable=True
    )

    op.alter_column(
        "tasks",
        "chapter_id",
        existing_type=sa.UUID(),
        nullable=True
    )

    op.alter_column(
        "tasks",
        "chapter_number",
        existing_type=sa.Integer(),
        nullable=True
    )


def downgrade():

    op.alter_column(
        "tasks",
        "batch_chapter_id",
        existing_type=sa.UUID(),
        nullable=False
    )

    op.alter_column(
        "tasks",
        "chapter_id",
        existing_type=sa.UUID(),
        nullable=False
    )

    op.alter_column(
        "tasks",
        "chapter_number",
        existing_type=sa.Integer(),
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
