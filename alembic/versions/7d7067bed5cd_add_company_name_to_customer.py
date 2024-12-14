"""Add company_name to Customer

Revision ID: 7d7067bed5cd
Revises: ea079ee1ee23
Create Date: 2024-12-14 20:05:07.284079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7d7067bed5cd'
down_revision = 'ea079ee1ee23'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('customers', sa.Column('company_name', sa.String(), nullable=False, server_default='Unknown'))

def downgrade():
    op.drop_column('customers', 'company_name')