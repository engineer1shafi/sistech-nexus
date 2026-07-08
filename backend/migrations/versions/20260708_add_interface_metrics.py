"""add interface_metrics table

Revision ID: 20260708_add_interface_metrics
Revises: 20260708_add_polling_policies
Create Date: 2026-07-08 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260708_add_interface_metrics'
down_revision = '20260708_add_polling_policies'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'interface_metrics',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('is_deleted', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('device_id', sa.UUID(as_uuid=True), sa.ForeignKey('devices.id', ondelete='CASCADE'), nullable=False),
        sa.Column('interface_id', sa.UUID(as_uuid=True), sa.ForeignKey('interfaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('admin_status', sa.String(length=30), nullable=True),
        sa.Column('oper_status', sa.String(length=30), nullable=True),
        sa.Column('rx_octets', sa.BigInteger, nullable=True),
        sa.Column('tx_octets', sa.BigInteger, nullable=True),
        sa.Column('rx_errors', sa.BigInteger, nullable=True),
        sa.Column('tx_errors', sa.BigInteger, nullable=True),
        sa.Column('rx_discards', sa.BigInteger, nullable=True),
        sa.Column('tx_discards', sa.BigInteger, nullable=True),
        sa.Column('speed', sa.BigInteger, nullable=True),
        sa.Column('utilization_in', sa.Float, nullable=True),
        sa.Column('utilization_out', sa.Float, nullable=True),
    )

    op.create_index('ix_interface_metrics_device_id', 'interface_metrics', ['device_id'])
    op.create_index('ix_interface_metrics_interface_id', 'interface_metrics', ['interface_id'])
    op.create_index('ix_interface_metrics_timestamp', 'interface_metrics', ['timestamp'])
    op.create_index('ix_interface_metrics_interface_id_timestamp', 'interface_metrics', ['interface_id', 'timestamp'])


def downgrade() -> None:
    op.drop_index('ix_interface_metrics_interface_id_timestamp', table_name='interface_metrics')
    op.drop_index('ix_interface_metrics_timestamp', table_name='interface_metrics')
    op.drop_index('ix_interface_metrics_interface_id', table_name='interface_metrics')
    op.drop_index('ix_interface_metrics_device_id', table_name='interface_metrics')
    op.drop_table('interface_metrics')
