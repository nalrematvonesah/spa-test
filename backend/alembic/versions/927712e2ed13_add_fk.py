"""add_fk

Revision ID: 927712e2ed13
Revises: e6ab308a1720
Create Date: 2026-04-24 05:52:34.125499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '927712e2ed13'
down_revision: Union[str, Sequence[str], None] = 'e6ab308a1720'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_foreign_key(
        'fk_parts_parent',
        'parts',
        'parts',
        ['parent_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
