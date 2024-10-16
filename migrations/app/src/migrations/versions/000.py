"""Create worker tables

Revision ID: 000
Revises:
Create Date: 2023-12-09 10:00:00

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table('workers',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('first_name', sa.String(), nullable=False),
                    sa.Column('last_name', sa.String(), nullable=False),
                    sa.Column('patronymic', sa.String(), nullable=True),
                    sa.Column('status', sa.String(), nullable=False, comment='1-уволен, 2-временно не работает, '
                                                                              '3-работает'),
                    sa.Column('category', sa.String(), nullable=False),
                    sa.Column('document', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('worker_phones',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('worker_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('phone', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['worker_id'], ['workers.id']),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('worker_phones')
    op.drop_table('workers')
