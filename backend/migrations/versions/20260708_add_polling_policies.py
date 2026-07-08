"""add polling_policies and device.polling_policy_id

Revision ID: 20260708_add_polling_policies
Revises: 20260708_add_neighbors_and_topology
Create Date: 2026-07-08 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260708_add_polling_policies'
down_revision = '20260708_add_neighbors_and_topology'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'polling_policies',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('is_deleted', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('name', sa.String(length=150), nullable=False, index=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('interval_seconds', sa.Integer, nullable=False, server_default='60'),
        sa.Column('timeout_seconds', sa.Integer, nullable=False, server_default='3'),
        sa.Column('retries', sa.Integer, nullable=False, server_default='2'),
        sa.Column('is_default', sa.Boolean, nullable=False, server_default=sa.text('false'), index=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default=sa.text('true'), index=True),
    )

    op.add_column('devices', sa.Column('polling_policy_id', sa.UUID(as_uuid=True), sa.ForeignKey('polling_policies.id'), nullable=True))


def downgrade() -> None:
    op.drop_column('devices', 'polling_policy_id')
    op.drop_table('polling_policies')
