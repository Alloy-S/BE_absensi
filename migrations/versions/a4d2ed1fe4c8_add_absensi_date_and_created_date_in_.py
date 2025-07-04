"""add absensi date and created date in approval koreksi

Revision ID: a4d2ed1fe4c8
Revises: 01b188861879
Create Date: 2025-06-14 22:06:50.298885

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a4d2ed1fe4c8'
down_revision = '01b188861879'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('approval_koreksi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('absensi_date', sa.Date(), nullable=False))
        batch_op.drop_column('date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('approval_koreksi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.drop_column('absensi_date')
        batch_op.drop_column('created_date')

    # ### end Alembic commands ###
