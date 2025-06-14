"""refactor name to fullname and add phone number

Revision ID: 612d08005087
Revises: 1655e5d9b267
Create Date: 2025-04-26 22:56:35.911769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '612d08005087'
down_revision = '1655e5d9b267'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fullname', sa.String(length=80), nullable=False))
        batch_op.add_column(sa.Column('phone', sa.String(length=16), nullable=False))
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
        batch_op.drop_column('phone')
        batch_op.drop_column('fullname')

    # ### end Alembic commands ###
