"""still working

Revision ID: b92b6f86a3c8
Revises: 555e27a9a943
Create Date: 2023-06-15 17:00:51.703951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b92b6f86a3c8'
down_revision = '555e27a9a943'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('_password_hash', sa.String(), nullable=False))
        batch_op.alter_column('weight',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('weight',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
        batch_op.drop_column('_password_hash')
        batch_op.drop_column('username')

    # ### end Alembic commands ###
