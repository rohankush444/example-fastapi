"""add last few columns to posts table

Revision ID: de4b32bce58f
Revises: 413ece0c25e9
Create Date: 2024-05-29 14:33:15.199580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de4b32bce58f'
down_revision: Union[str, None] = '413ece0c25e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column(
        'published',sa.Boolean(),nullable=False,server_default='True'))
    op.add_column('posts',sa.Column(
        'created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
