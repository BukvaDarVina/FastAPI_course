"""add colums users table

Revision ID: c35792ba1aca
Revises: 731546103ae2
Create Date: 2024-11-19 11:33:36.402013

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c35792ba1aca"
down_revision: Union[str, None] = "731546103ae2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
