"""add content column to posts table

Revision ID: f04cb6160261
Revises: be8b4de39eea
Create Date: 2025-05-03 12:51:22.034969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f04cb6160261'
down_revision: Union[str, None] = 'be8b4de39eea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("content", sa.String, nullable=False),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
