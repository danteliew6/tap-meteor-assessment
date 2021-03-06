"""empty message

Revision ID: 148ead86e545
Revises: 2f8de6f7a8b6
Create Date: 2022-07-11 00:40:15.653435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '148ead86e545'
down_revision = '2f8de6f7a8b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('households',
    sa.Column('household_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('household_type', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('household_id'),
    mysql_auto_increment='1',
    mysql_engine='InnoDB'
    )
    op.create_table('family_members',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('marital_status', sa.String(length=20), nullable=True),
    sa.Column('occupation_type', sa.String(length=20), nullable=True),
    sa.Column('annual_income', sa.Float(), nullable=True),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('household_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['household_id'], ['households.household_id'], ),
    sa.PrimaryKeyConstraint('name'),
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('family_members')
    op.drop_table('households')
    # ### end Alembic commands ###
