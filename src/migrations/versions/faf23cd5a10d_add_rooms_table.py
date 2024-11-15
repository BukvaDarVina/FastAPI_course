"""add rooms table

Revision ID: faf23cd5a10d
Revises: b488404a614b
Create Date: 2024-11-15 10:40:30.147670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'faf23cd5a10d'
down_revision: Union[str, None] = 'b488404a614b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rooms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('hotel_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('price', sa.Integer(), nullable=False),
                    sa.Column('quantity', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('rooms')
