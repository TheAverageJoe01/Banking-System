"""Add datetime

Revision ID: a549058b7d3d
Revises: 0238d8953886
Create Date: 2024-05-01 20:32:56.067004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a549058b7d3d'
down_revision: Union[str, None] = '0238d8953886'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
