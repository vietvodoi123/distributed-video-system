"""add batch cleanup status

Revision ID: b6c585cb9583
Revises: a636dd875fa1
Create Date: 2026-07-07 23:42:18.035991

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6c585cb9583'
down_revision: Union[str, Sequence[str], None] = 'a636dd875fa1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "batches",
        sa.Column(
            "cleanup_status",
            sa.String(),
            nullable=False,
            server_default="none"
        )
    )


def downgrade():

    op.drop_column(
        "batches",
        "cleanup_status"
    )
