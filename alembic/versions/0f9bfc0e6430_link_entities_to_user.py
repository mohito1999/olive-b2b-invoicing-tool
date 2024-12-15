from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0f9bfc0e6430'
down_revision = 'c5f63e9ef35f'
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Add the user_id column as nullable
    op.add_column('transactions', sa.Column('user_id', sa.Integer(), nullable=True))
    
    # Step 2: Populate the user_id column for existing rows
    op.execute("UPDATE transactions SET user_id = 1 WHERE user_id IS NULL")

    # Step 3: Make the user_id column non-nullable
    op.alter_column('transactions', 'user_id', nullable=False)
    op.create_foreign_key('fk_transactions_user', 'transactions', 'users', ['user_id'], ['id'])

    # Repeat similar steps for other tables if needed
    op.add_column('invoices', sa.Column('user_id', sa.Integer(), nullable=True))
    # Populate user_id for invoices
    op.execute("UPDATE invoices SET user_id = 1 WHERE user_id IS NULL")
    op.alter_column('invoices', 'user_id', nullable=False)
    op.create_foreign_key('fk_invoices_user', 'invoices', 'users', ['user_id'], ['id'])

def downgrade():
    # Reverse the changes made in upgrade
    op.drop_constraint('fk_transactions_user', 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'user_id')

    op.drop_constraint('fk_invoices_user', 'invoices', type_='foreignkey')
    op.drop_column('invoices', 'user_id')