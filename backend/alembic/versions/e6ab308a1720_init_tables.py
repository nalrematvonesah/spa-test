"""init_tables

Revision ID: e6ab308a1720
Revises: 
Create Date: 2026-04-24 05:51:53.613824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6ab308a1720'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'parts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('price', sa.Float()),
        sa.Column('quantity', sa.Integer()),
        sa.Column('parent_id', sa.Integer(), nullable=True),
    )

    op.create_table(
        'part_history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('part_id', sa.Integer()),
        sa.Column('action', sa.String()),
        sa.Column('timestamp', sa.DateTime()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
