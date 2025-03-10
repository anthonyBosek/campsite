"""update models

Revision ID: 5a2512db59e0
Revises: 0c045b4b4e0d
Create Date: 2023-11-20 19:34:13.201689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a2512db59e0'
down_revision = '0c045b4b4e0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('campsites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('park_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('max_capacity', sa.Integer(), nullable=True))
        batch_op.drop_column('max_capcity')
        batch_op.drop_column('park_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('campsites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('park_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('max_capcity', sa.INTEGER(), nullable=True))
        batch_op.drop_column('max_capacity')
        batch_op.drop_column('park_name')

    # ### end Alembic commands ###
