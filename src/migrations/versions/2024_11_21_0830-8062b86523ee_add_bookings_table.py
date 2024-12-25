"""add bookings table

Revision ID: 8062b86523ee
Revises: 12b40bd2013f
Create Date: 2024-11-21 08:30:35.019431

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8062b86523ee"
down_revision: Union[str, None] = "12b40bd2013f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["nickname"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
