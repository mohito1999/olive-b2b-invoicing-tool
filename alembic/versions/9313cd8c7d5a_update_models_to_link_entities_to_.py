from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9313cd8c7d5a'
down_revision = '0f9bfc0e6430'  # Replace with the actual previous revision ID
branch_labels = None
depends_on = None



def upgrade() -> None:
    # Drop foreign key constraints
    op.drop_constraint('invoices_customer_id_fkey', 'invoices', type_='foreignkey')
    op.drop_constraint('fk_invoices_organization', 'invoices', type_='foreignkey')
    op.drop_constraint('fk_invoices_user', 'invoices', type_='foreignkey')
    
    # Make necessary schema changes here
    # For example, if you need to add a new column or modify an existing one

    # Recreate foreign key constraints with updated relationships
    op.create_foreign_key('invoices_customer_id_fkey', 'invoices', 'customers', ['customer_id'], ['id'])
    op.create_foreign_key('fk_invoices_organization', 'invoices', 'organizations', ['organization_id'], ['id'])
    # Remove the user_id foreign key if not needed anymore
    # op.create_foreign_key('fk_invoices_user', 'invoices', 'users', ['user_id'], ['id'])

def downgrade() -> None:
    # Reverse the changes made in the upgrade function
    op.drop_constraint('invoices_customer_id_fkey', 'invoices', type_='foreignkey')
    op.drop_constraint('fk_invoices_organization', 'invoices', type_='foreignkey')
    # op.drop_constraint('fk_invoices_user', 'invoices', type_='foreignkey')

    # Recreate the original foreign key constraints
    op.create_foreign_key('invoices_customer_id_fkey', 'invoices', 'customers', ['customer_id'], ['id'])
    op.create_foreign_key('fk_invoices_organization', 'invoices', 'organizations', ['organization_id'], ['id'])
    op.create_foreign_key('fk_invoices_user', 'invoices', 'users', ['user_id'], ['id'])