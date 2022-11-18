"""added admin table

Revision ID: 9bb61973bead
Revises: 4a3cf1b621d4
Create Date: 2022-10-24 21:01:52.868865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bb61973bead'
down_revision = '4a3cf1b621d4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('emailAddress', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='CCC'
    )
    op.create_index(op.f('ix_CCC_admin_id'), 'admin', ['id'], unique=False, schema='CCC')


def downgrade() -> None:
    op.drop_index(op.f('ix_CCC_admin_id'), table_name='admin', schema='CCC')
    op.drop_table('admin', schema='CCC')
