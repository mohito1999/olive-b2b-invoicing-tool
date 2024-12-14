"""Add phone_number to Customer

Revision ID: de82251cb724
Revises: 3d014bc80353
Create Date: 2024-12-14 20:15:53.710204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'de82251cb724'
down_revision: Union[str, None] = '3d014bc80353'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
       op.add_column('customers', sa.Column('phone_number', sa.String(), nullable=True))

def downgrade():
    op.drop_column('customers', 'phone_number')