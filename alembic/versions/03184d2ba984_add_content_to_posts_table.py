"""add content to posts table

Revision ID: 03184d2ba984
Revises: 7a371f11aefb
Create Date: 2024-05-29 14:21:14.022674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03184d2ba984'
down_revision: Union[str, None] = '7a371f11aefb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
