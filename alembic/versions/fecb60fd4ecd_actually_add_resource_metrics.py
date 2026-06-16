"""actually add resource_metrics

Revision ID: fecb60fd4ecd
Revises: 3eb30a1eb2c9
Create Date: 2026-05-29 20:12:17.428859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fecb60fd4ecd'
down_revision: Union[str, Sequence[str], None] = '3eb30a1eb2c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(

        "tasks",

        sa.Column(
            "resource_metrics",
            postgresql.JSONB(),
            nullable=True
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
