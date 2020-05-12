"""empty message

Revision ID: 5635f4622a65
Revises: 5c8438d6bf11
Create Date: 2020-05-11 19:32:09.088733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5635f4622a65'
down_revision = '5c8438d6bf11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subnet',
    sa.Column('ip', sa.String(), nullable=False),
    sa.Column('allowed', sa.Boolean(), nullable=True),
    sa.Column('start_of_restriction', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('ip')
    )
    op.alter_column('request', 'number',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'request', 'subnet', ['ip'], ['ip'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'request', type_='foreignkey')
    op.alter_column('request', 'number',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_table('subnet')
    # ### end Alembic commands ###