"""add resource_metrics to tasks

Revision ID: 3eb30a1eb2c9
Revises: d60fe7be23d9
Create Date: 2026-05-29 20:04:52.159284

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3eb30a1eb2c9'
down_revision: Union[str, Sequence[str], None] = 'd60fe7be23d9'
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


def downgrade():

    op.drop_column(

        "tasks",

        "resource_metrics"
    )
