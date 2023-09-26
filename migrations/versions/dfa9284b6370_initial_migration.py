"""Initial migration

Revision ID: dfa9284b6370
Revises: 
Create Date: 2023-09-23 22:31:44.705559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = 'dfa9284b6370'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('surname', sa.String(length=255), nullable=True),
    sa.Column('birthdate', sa.Date(), nullable=False),
    sa.Column('number_employee', sa.String(length=8), nullable=False),
    sa.Column('curp', sa.String(length=18), nullable=False),
    sa.Column('ssn', sa.String(length=11), nullable=False),
    sa.Column('phone', sa.String(length=10), nullable=False),
    sa.Column('nationality', sa.String(length=255), nullable=False),
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=1), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('beneficiaries',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('surname', sa.String(length=255), nullable=True),
    sa.Column('birthdate', sa.Date(), nullable=False),
    sa.Column('curp', sa.String(length=18), nullable=False),
    sa.Column('ssn', sa.String(length=11), nullable=False),
    sa.Column('phone', sa.String(length=10), nullable=False),
    sa.Column('nationality', sa.String(length=255), nullable=False),
    sa.Column('participation_percentage', sa.SmallInteger(), nullable=False),
    sa.Column('employee_id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('id', mssql.UNIQUEIDENTIFIER(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=1), nullable=False),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('beneficiaries')
    op.drop_table('employees')
    # ### end Alembic commands ###
