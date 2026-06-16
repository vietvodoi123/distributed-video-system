"""make task chapter refs nullable

Revision ID: e84a975928c8
Revises: db706f652605
Create Date: 2026-05-24 16:01:02.604821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e84a975928c8'
down_revision: Union[str, Sequence[str], None] = 'db706f652605'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
