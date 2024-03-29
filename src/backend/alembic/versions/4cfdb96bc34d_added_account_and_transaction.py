"""Added account and transaction

Revision ID: 4cfdb96bc34d
Revises: 2881204d8f1a
Create Date: 2024-03-29 13:08:33.375769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cfdb96bc34d'
down_revision: Union[str, None] = '2881204d8f1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
