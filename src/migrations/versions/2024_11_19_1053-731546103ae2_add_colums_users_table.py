"""add colums users table

Revision ID: 731546103ae2
Revises: b96f8e906c87
Create Date: 2024-11-19 10:53:18.666666

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "731546103ae2"
down_revision: Union[str, None] = "b96f8e906c87"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users", "nickname", existing_type=sa.VARCHAR(length=100), nullable=True
    )
    op.alter_column(
        "users", "first_name", existing_type=sa.VARCHAR(length=150), nullable=True
    )
    op.alter_column(
        "users", "last_name", existing_type=sa.VARCHAR(length=150), nullable=True
    )


def downgrade() -> None:
    op.alter_column(
        "users", "last_name", existing_type=sa.VARCHAR(length=150), nullable=False
    )
    op.alter_column(
        "users", "first_name", existing_type=sa.VARCHAR(length=150), nullable=False
    )
    op.alter_column(
        "users", "nickname", existing_type=sa.VARCHAR(length=100), nullable=False
    )
