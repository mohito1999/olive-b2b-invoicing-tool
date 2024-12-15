from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '16a82d8e8f9a'
down_revision = 'de82251cb724'
branch_labels = None
depends_on = None

def upgrade():
    # Add organization_id column to invoices table
    op.add_column('invoices', sa.Column('organization_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_invoices_organization', 'invoices', 'organizations', ['organization_id'], ['id'])

    # Repeat similar steps for other tables that need the organization_id column
    op.add_column('transactions', sa.Column('organization_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_transactions_organization', 'transactions', 'organizations', ['organization_id'], ['id'])

    op.add_column('invoice_items', sa.Column('organization_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_invoice_items_organization', 'invoice_items', 'organizations', ['organization_id'], ['id'])

    # Add organization_id to other tables as needed

def downgrade():
    # Remove organization_id column from invoices table
    op.drop_constraint('fk_invoices_organization', 'invoices', type_='foreignkey')
    op.drop_column('invoices', 'organization_id')

    # Repeat similar steps for other tables
    op.drop_constraint('fk_transactions_organization', 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'organization_id')

    op.drop_constraint('fk_invoice_items_organization', 'invoice_items', type_='foreignkey')
    op.drop_column('invoice_items', 'organization_id')

    # Remove organization_id from other tables as needed