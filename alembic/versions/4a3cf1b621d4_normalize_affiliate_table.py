"""normalize affiliate table

Revision ID: 4a3cf1b621d4
Revises: 0c5ab70ef25b
Create Date: 2022-10-20 19:48:33.982002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a3cf1b621d4'
down_revision = '0c5ab70ef25b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("affiliate", "totalCarsOffRoad", "CCC")
    op.drop_column("affiliate", "totalFightingFoodWaste", "CCC")
    op.drop_column("affiliate", "totalWaterSaved", "CCC")
    op.drop_column("affiliate", "totalLandUse", "CCC")
    op.drop_column("affiliate", "totalCholesterolSaved", "CCC")


def downgrade() -> None:
    op.add_column("affiliate", sa.Column('totalCarsOffRoad', sa.Float(), nullable=True), "CCC")
    op.add_column("affiliate", sa.Column('totalFightingFoodWaste', sa.Float(), nullable=True), "CCC")
    op.add_column("affiliate", sa.Column('totalWaterSaved', sa.Float(), nullable=True), "CCC")
    op.add_column("affiliate", sa.Column('totalLandUse', sa.Float(), nullable=True), "CCC")
    op.add_column("affiliate", sa.Column('totalCholesterolSaved', sa.Float(), nullable=True), "CCC")
