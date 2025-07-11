"""Added zone

Revision ID: c25bd8b53d84
Revises: 224634ecd827
Create Date: 2025-03-13 07:45:52.299658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c25bd8b53d84'
down_revision: Union[str, None] = '224634ecd827'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('services', sa.Column('platform', sa.String(), nullable=True))
    op.add_column('services', sa.Column('zone', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('services', 'zone')
    op.drop_column('services', 'platform')
    # ### end Alembic commands ###
