"""make story channel required

Revision ID: db706f652605
Revises: 931d9056dd7f
Create Date: 2026-05-23 16:26:35.191702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db706f652605'
down_revision: Union[str, Sequence[str], None] = '931d9056dd7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.alter_column(
        'stories',
        'channel_id',
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
