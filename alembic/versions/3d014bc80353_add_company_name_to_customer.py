"""Add company_name to Customer

Revision ID: 3d014bc80353
Revises: 7d7067bed5cd
Create Date: 2024-12-14 19:30:00

"""
from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision = "3d014bc80353"
down_revision = "7d7067bed5cd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add company_name to the customers table
    op.add_column("customers", sa.Column("company_name", sa.String(), nullable=True))


def downgrade() -> None:
    # Remove company_name on downgrade
    op.drop_column("customers", "company_name")
