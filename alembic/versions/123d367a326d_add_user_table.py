"""add user table

Revision ID: 123d367a326d
Revises: e94a43572229
Create Date: 2025-05-04 21:45:17.965986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '123d367a326d'
down_revision: Union[str, None] = 'e94a43572229'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("email", sa.String(), nullable=False, unique=True),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )    
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_table("users")
    """Downgrade schema."""
    pass
