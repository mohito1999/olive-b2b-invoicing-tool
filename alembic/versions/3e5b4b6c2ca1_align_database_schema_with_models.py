"""Align database schema with models

Revision ID: 3e5b4b6c2ca1
Revises: 9313cd8c7d5a
Create Date: 2024-12-15 00:52:33.142358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3e5b4b6c2ca1'
down_revision: Union[str, None] = '9313cd8c7d5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop foreign key constraints
    op.drop_constraint('fk_transactions_user', 'transactions', type_='foreignkey')
    
    # Make necessary schema changes here
    # For example, if you need to add a new column or modify an existing one

    # Recreate foreign key constraints with updated relationships
    op.create_foreign_key('fk_transactions_user', 'transactions', 'users', ['user_id'], ['id'])

def downgrade() -> None:
    # Reverse the changes made in the upgrade function
    op.drop_constraint('fk_transactions_user', 'transactions', type_='foreignkey')

    # Recreate the original foreign key constraints
    op.create_foreign_key('fk_transactions_user', 'transactions', 'users', ['user_id'], ['id'])