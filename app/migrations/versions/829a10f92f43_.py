"""empty message

Revision ID: 829a10f92f43
Revises: 7043f317fbd3
Create Date: 2020-05-10 17:26:40.065907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '829a10f92f43'
down_revision = '7043f317fbd3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ip', sa.Column('ip', sa.String(), nullable=False))
    op.drop_column('ip', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ip', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('ip', 'ip')
    # ### end Alembic commands ###