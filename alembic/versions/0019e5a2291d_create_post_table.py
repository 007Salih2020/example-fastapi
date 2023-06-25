"""create post table

Revision ID: 0019e5a2291d
Revises: 
Create Date: 2023-06-25 12:15:12.139519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0019e5a2291d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
