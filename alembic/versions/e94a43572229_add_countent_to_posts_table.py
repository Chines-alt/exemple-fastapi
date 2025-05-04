"""add countent to posts table

Revision ID: e94a43572229
Revises: 4af57f2d34f4
Create Date: 2025-05-04 21:13:30.439088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e94a43572229'
down_revision: Union[str, None] = '4af57f2d34f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    """Downgrade schema."""
    pass
