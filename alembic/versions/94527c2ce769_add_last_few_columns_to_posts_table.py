"""add last few columns to posts table

Revision ID: 94527c2ce769
Revises: 11937475d259
Create Date: 2025-05-04 21:59:56.685368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94527c2ce769'
down_revision: Union[str, None] = '11937475d259'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))

   
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    """Downgrade schema."""
    pass
