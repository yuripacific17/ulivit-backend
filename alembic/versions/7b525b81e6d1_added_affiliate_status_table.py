"""Added affiliate status table

Revision ID: 7b525b81e6d1
Revises: 9bb61973bead
Create Date: 2022-11-03 18:44:12.247585

"""
from uuid import UUID

import sqlalchemy as sa
from alembic import op
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = '7b525b81e6d1'
down_revision = '9bb61973bead'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('affiliate_status',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('status'),
    schema='CCC'
    )
    op.add_column('affiliate',
    sa.Column('statusId', postgresql.UUID(as_uuid=True), ForeignKey('CCC.affiliate_status.id'), nullable=True),
    schema='CCC'
    )

    # create a table for bulk insert
    affiliate_status_table = table('affiliate_status',
                                   column('id', postgresql.UUID(as_uuid=True)),
                                   column('status', String),
                                   schema='CCC')
    op.bulk_insert(affiliate_status_table,
                   [
                       {
                           'id': UUID('079434f9-732e-425b-981e-82157f6e0801'),
                           'status': 'pending'
                       },
                       {
                           'id': UUID('f36a54a2-cf5d-4b20-b379-09a938120685'),
                           'status': 'approved'
                       }
                   ]
                   )


def downgrade() -> None:
    op.drop_column('affiliate', 'statusId', schema='CCC')
    op.drop_table('affiliate_status', schema='CCC')
