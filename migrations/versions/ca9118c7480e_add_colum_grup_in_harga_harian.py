"""add colum grup in harga harian

Revision ID: ca9118c7480e
Revises: 552ccf452b5a
Create Date: 2025-06-22 19:32:23.870074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca9118c7480e'
down_revision = '552ccf452b5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('harga_harian_borongan', schema=None) as batch_op:
        batch_op.add_column(sa.Column('grup_harga', sa.UUID(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('harga_harian_borongan', schema=None) as batch_op:
        batch_op.drop_column('grup_harga')

    # ### end Alembic commands ###
