"""Initial migration

Revision ID: 176484337cb3
Revises: 
Create Date: 2023-03-28 13:15:10.907672

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '176484337cb3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('contents', sa.String(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
