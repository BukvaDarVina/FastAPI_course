"""add timestamp in bookings table

Revision ID: 63f94e2c614b
Revises: 8062b86523ee
Create Date: 2024-11-21 11:33:38.303101

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "63f94e2c614b"
down_revision: Union[str, None] = "8062b86523ee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("bookings", sa.Column("create_at", sa.DateTime(), nullable=False))


def downgrade() -> None:
    op.drop_column("bookings", "create_at")
