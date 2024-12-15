from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = '5ccf21e76ce2'
down_revision = '56d060339ed2'
branch_labels = None
depends_on = None


def check_constraint_exists(table_name, constraint_name):
    conn = op.get_bind()
    inspector = inspect(conn)
    constraints = inspector.get_foreign_keys(table_name)
    return any(fk['name'] == constraint_name for fk in constraints)


def check_column_exists(table_name, column_name):
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = inspector.get_columns(table_name)
    return any(col['name'] == column_name for col in columns)


def upgrade():
    # Remove user_id from tables if they exist
    for table in ['customers', 'transactions', 'invoices']:
        if check_column_exists(table, 'user_id'):
            op.drop_column(table, 'user_id')

    # Add organization_id to tables if they don't exist
    tables_to_update = ['customers', 'users', 'inventory', 'invoice_items', 'transactions', 'invoices']
    for table in tables_to_update:
        if not check_column_exists(table, 'organization_id'):
            op.add_column(table, sa.Column('organization_id', sa.Integer(), nullable=False))

    # Add foreign key constraints if they don't exist
    foreign_keys = {
        'customers': 'fk_customers_organization',
        'users': 'fk_users_organization',
        'inventory': 'fk_inventory_organization',
        'invoice_items': 'fk_invoice_items_organization',
        'transactions': 'fk_transactions_organization',
        'invoices': 'fk_invoices_organization',
    }

    for table, fk_name in foreign_keys.items():
        if not check_constraint_exists(table, fk_name):
            op.create_foreign_key(fk_name, table, 'organizations', ['organization_id'], ['id'])


def downgrade():
    foreign_keys = {
        'customers': 'fk_customers_organization',
        'users': 'fk_users_organization',
        'inventory': 'fk_inventory_organization',
        'invoice_items': 'fk_invoice_items_organization',
        'transactions': 'fk_transactions_organization',
        'invoices': 'fk_invoices_organization',
    }

    for table, fk_name in foreign_keys.items():
        if check_constraint_exists(table, fk_name):
            op.drop_constraint(fk_name, table, type_='foreignkey')

    tables_to_update = ['customers', 'users', 'inventory', 'invoice_items', 'transactions', 'invoices']
    for table in tables_to_update:
        if check_column_exists(table, 'organization_id'):
            op.drop_column(table, 'organization_id')

    for table in ['customers', 'transactions', 'invoices']:
        if not check_column_exists(table, 'user_id'):
            op.add_column(table, sa.Column('user_id', sa.Integer(), nullable=True))
