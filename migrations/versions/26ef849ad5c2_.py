"""empty message

Revision ID: 26ef849ad5c2
Revises: 32cb32d0e0d7
Create Date: 2020-11-18 13:08:06.272774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26ef849ad5c2'
down_revision = '32cb32d0e0d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'created_at')
    # ### end Alembic commands ###
