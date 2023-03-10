"""empty message

Revision ID: acb1bd0886cd
Revises: fbd76c6e268d
Create Date: 2023-01-12 20:03:38.027626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acb1bd0886cd'
down_revision = 'fbd76c6e268d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    # ### end Alembic commands ###
