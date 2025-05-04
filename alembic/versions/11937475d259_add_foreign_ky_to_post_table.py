"""add foreign-ky to post table

Revision ID: 11937475d259
Revises: 123d367a326d
Create Date: 2025-05-04 21:51:55.005367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11937475d259'
down_revision: Union[str, None] = '123d367a326d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users", local_cols=["owner_id"],
                           remote_cols=["id"], ondelete="CASCADE")
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    """Downgrade schema."""
    pass
