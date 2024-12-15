"""Add organization_id to users

Revision ID: c5f63e9ef35f
Revises: 16a82d8e8f9a
Create Date: 2024-12-15 00:10:44.741096

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c5f63e9ef35f'
down_revision = '16a82d8e8f9a'
branch_labels = None
depends_on = None

def upgrade():
    # Add organization_id column to users table
    op.add_column('users', sa.Column('organization_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_users_organization', 'users', 'organizations', ['organization_id'], ['id'])

def downgrade():
    # Remove organization_id column from users table
    op.drop_constraint('fk_users_organization', 'users', type_='foreignkey')
    op.drop_column('users', 'organization_id')