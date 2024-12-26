"""add facilities

Revision ID: 6172f0825444
Revises: 5daf305fcd13
Create Date: 2024-11-22 11:06:15.830658

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6172f0825444"
down_revision: Union[str, None] = "5daf305fcd13"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("room_facilities", sa.Column("facilities_id", sa.Integer(), nullable=False))
    op.drop_constraint("room_facilities_facilities_fkey", "room_facilities", type_="foreignkey")
    op.create_foreign_key(None, "room_facilities", "facilities", ["facilities_id"], ["id"])
    op.drop_column("room_facilities", "facilities")


def downgrade() -> None:
    op.add_column(
        "room_facilities",
        sa.Column("facilities", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "room_facilities", type_="foreignkey")
    op.create_foreign_key(
        "room_facilities_facilities_fkey",
        "room_facilities",
        "facilities",
        ["facilities"],
        ["id"],
    )
    op.drop_column("room_facilities", "facilities_id")
