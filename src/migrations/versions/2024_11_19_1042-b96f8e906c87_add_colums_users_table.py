"""add colums users table

Revision ID: b96f8e906c87
Revises: 8efccd6eb231
Create Date: 2024-11-19 10:42:56.906265

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b96f8e906c87"
down_revision: Union[str, None] = "8efccd6eb231"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("nickname", sa.String(length=100), nullable=False))
    op.add_column(
        "users", sa.Column("first_name", sa.String(length=150), nullable=False)
    )
    op.add_column(
        "users", sa.Column("last_name", sa.String(length=150), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
    op.drop_column("users", "nickname")
