"""Add gst_percentage to invoice_items

Revision ID: 2fb905031a89
Revises: 5ccf21e76ce2
Create Date: 2024-12-15 01:54:27.707732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fb905031a89'
down_revision = '5ccf21e76ce2'
branch_labels = None
depends_on = None


def upgrade():
    # Add gst_percentage column to invoice_items table
    op.add_column('invoice_items', sa.Column('gst_percentage', sa.Float(), nullable=True))


def downgrade():
    # Remove gst_percentage column from invoice_items table
    op.drop_column('invoice_items', 'gst_percentage')