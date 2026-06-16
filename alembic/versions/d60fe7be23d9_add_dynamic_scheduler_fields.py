"""add dynamic scheduler fields

Revision ID: d60fe7be23d9
Revises: fe42584b72f7
Create Date: 2026-05-28 23:33:49.700999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd60fe7be23d9'
down_revision: Union[str, Sequence[str], None] = 'fe42584b72f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # =====================================
    # TASKS
    # =====================================

    op.add_column(
        "tasks",
        sa.Column(
            "resource_requirements",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True
        )
    )

    op.add_column(
        "tasks",
        sa.Column(
            "dynamic_cost",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "tasks",
        sa.Column(
            "estimated_duration",
            sa.Integer(),
            nullable=True
        )
    )

    # =====================================
    # WORKERS
    # =====================================

    op.add_column(
        "workers",
        sa.Column(
            "resource_weights",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True
        )
    )

    op.add_column(
        "workers",
        sa.Column(
            "resource_capacity",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True
        )
    )

    op.add_column(
        "workers",
        sa.Column(
            "current_load",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True
        )
    )

    op.add_column(
        "workers",
        sa.Column(
            "current_dynamic_cost",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "workers",
        sa.Column(
            "max_dynamic_cost",
            sa.Float(),
            nullable=True
        )
    )


def downgrade():

    # TASKS

    op.drop_column(
        "tasks",
        "resource_requirements"
    )

    op.drop_column(
        "tasks",
        "dynamic_cost"
    )

    op.drop_column(
        "tasks",
        "estimated_duration"
    )

    # WORKERS

    op.drop_column(
        "workers",
        "resource_weights"
    )

    op.drop_column(
        "workers",
        "resource_capacity"
    )

    op.drop_column(
        "workers",
        "current_load"
    )

    op.drop_column(
        "workers",
        "current_dynamic_cost"
    )

    op.drop_column(
        "workers",
        "max_dynamic_cost"
    )
