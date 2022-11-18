"""promo code can be null for affiliate table

Revision ID: 157a4b38fa07
Revises: 7b525b81e6d1
Create Date: 2022-11-16 21:13:14.959573

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '157a4b38fa07'
down_revision = '7b525b81e6d1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('affiliate', 'promoCode', nullable=True, schema='CCC')


def downgrade() -> None:
    op.alter_column('affiliate', 'promoCode', nullable=False, schema='CCC')
