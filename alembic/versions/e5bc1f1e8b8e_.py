"""empty message

Revision ID: e5bc1f1e8b8e
Revises: 5a57ee0d7001
Create Date: 2020-06-03 22:36:59.374606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5bc1f1e8b8e'
down_revision = '5a57ee0d7001'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sync_players',
    sa.Column('player_ign', sa.String(length=256), nullable=False),
    sa.Column('shard', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('player_ign', 'shard')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sync_players')
    # ### end Alembic commands ###
