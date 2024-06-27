"""add content column

Revision ID: f5b3aec63c1b
Revises: f7d270f4c329
Create Date: 2024-06-27 10:56:42.862709

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f5b3aec63c1b"
down_revision: Union[str, None] = "f7d270f4c329"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
