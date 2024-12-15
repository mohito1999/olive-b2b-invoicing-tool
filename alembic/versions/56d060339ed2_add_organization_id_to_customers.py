from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '56d060339ed2'
down_revision = '3e5b4b6c2ca1'
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Add the column as nullable
    op.add_column('customers', sa.Column('organization_id', sa.Integer(), nullable=True))
    
    # Step 2: Populate the column with the default organization ID
    op.execute('UPDATE customers SET organization_id = 1 WHERE organization_id IS NULL')

    # Step 3: Make the column non-nullable
    op.alter_column('customers', 'organization_id', existing_type=sa.Integer(), nullable=False)
    op.create_foreign_key('fk_customers_organization_id', 'customers', 'organizations', ['organization_id'], ['id'])

def downgrade():
    op.drop_constraint('fk_customers_organization_id', 'customers', type_='foreignkey')
    op.drop_column('customers', 'organization_id')