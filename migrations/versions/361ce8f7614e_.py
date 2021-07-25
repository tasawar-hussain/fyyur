"""empty message

Revision ID: 361ce8f7614e
Revises: 629864f6eb49
Create Date: 2021-07-26 00:42:21.440869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '361ce8f7614e'
down_revision = '629864f6eb49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('genres', sa.ARRAY(sa.String()), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'genres')
    # ### end Alembic commands ###
