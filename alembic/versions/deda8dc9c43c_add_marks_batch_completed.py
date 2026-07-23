"""add marks_batch_completed

Revision ID: deda8dc9c43c
Revises: b51c499139aa
Create Date: 2026-07-23 09:33:53.683010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'deda8dc9c43c'
down_revision: Union[str, Sequence[str], None] = 'b51c499139aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column(
            "marks_batch_completed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    op.alter_column(
        "tasks",
        "marks_batch_completed",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column(
        "tasks",
        "marks_batch_completed",
    )
