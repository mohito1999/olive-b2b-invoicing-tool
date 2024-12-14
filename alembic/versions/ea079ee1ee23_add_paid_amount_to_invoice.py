"""Add paid_amount to Invoice

Revision ID: ea079ee1ee23
Revises: 
Create Date: 2024-12-14 19:00:13.628510

"""
from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision = "ea079ee1ee23"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the `paid_amount` column to the `invoices` table
    op.add_column("invoices", sa.Column("paid_amount", sa.Float, nullable=True))


def downgrade() -> None:
    # Remove the `paid_amount` column on downgrade
    op.drop_column("invoices", "paid_amount")
