"""make task chapter refs nullable

Revision ID: b60e5acccc40
Revises: e84a975928c8
Create Date: 2026-05-24 16:01:38.233188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b60e5acccc40'
down_revision: Union[str, Sequence[str], None] = 'e84a975928c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
