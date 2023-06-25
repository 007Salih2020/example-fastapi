"""create new column

Revision ID: 0180f8d79edf
Revises: 0019e5a2291d
Create Date: 2023-06-25 12:25:40.056829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0180f8d79edf'
down_revision = '0019e5a2291d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    
    pass


def downgrade() -> None:
    pass
