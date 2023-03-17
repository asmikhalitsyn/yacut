"""added added_by field

Revision ID: 958ac4d42907
Revises: 
Create Date: 2023-03-17 12:32:20.264316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '958ac4d42907'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original', sa.String(length=1024), nullable=False),
    sa.Column('short', sa.String(length=16), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short')
    )
    op.create_index(op.f('ix_url_map_timestamp'), 'url_map', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_url_map_timestamp'), table_name='url_map')
    op.drop_table('url_map')
    # ### end Alembic commands ###