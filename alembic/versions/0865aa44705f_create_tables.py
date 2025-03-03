"""Create Tables

Revision ID: 0865aa44705f
Revises: 
Create Date: 2025-03-03 13:44:57.051782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0865aa44705f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number', sa.String(),nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
