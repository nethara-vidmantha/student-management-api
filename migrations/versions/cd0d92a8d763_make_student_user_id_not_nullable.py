"""make student user_id not nullable

Revision ID: cd0d92a8d763
Revises: 67c24b0b8628
Create Date: 2026-11-22 15:51:50.061424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd0d92a8d763'
down_revision: Union[str, Sequence[str], None] = '67c24b0b8628'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.alter_column(
        'students',
        'user_id',
        existing_type=sa.Integer(),
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
