"""initial migration

Revision ID: efddd557c422
Revises: 673dfcf12515
Create Date: 2026-08-25 17:40:10.645877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efddd557c422'
down_revision: Union[str, Sequence[str], None] = '673dfcf12515'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
