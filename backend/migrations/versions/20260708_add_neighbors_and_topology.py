"""add neighbors and topology_links tables

Revision ID: 20260708_add_neighbors_and_topology
Revises: 172e602748b4
Create Date: 2026-07-08 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260708_add_neighbors_and_topology'
down_revision = '172e602748b4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'neighbors',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('is_deleted', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('local_device_id', sa.UUID(as_uuid=True), sa.ForeignKey('devices.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('local_interface_id', sa.UUID(as_uuid=True), sa.ForeignKey('interfaces.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('protocol', sa.String(length=30), nullable=False, server_default='LLDP'),
        sa.Column('remote_chassis_id', sa.String(length=255), nullable=True),
        sa.Column('remote_port_id', sa.String(length=255), nullable=True),
        sa.Column('remote_system_name', sa.String(length=255), nullable=True),
        sa.Column('remote_system_description', sa.Text, nullable=True),
        sa.Column('remote_management_address', sa.String(length=255), nullable=True),
        sa.Column('remote_capabilities', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default=sa.text('true'), index=True),
    )

    op.create_table(
        'topology_links',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('is_deleted', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('source_device_id', sa.UUID(as_uuid=True), sa.ForeignKey('devices.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('source_interface_id', sa.UUID(as_uuid=True), sa.ForeignKey('interfaces.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('target_device_id', sa.UUID(as_uuid=True), sa.ForeignKey('devices.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('target_interface_id', sa.UUID(as_uuid=True), sa.ForeignKey('interfaces.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('protocol', sa.String(length=30), nullable=False, server_default='LLDP'),
        sa.Column('confidence', sa.Integer, nullable=False, server_default='50'),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default=sa.text('true'), index=True),
    )


def downgrade() -> None:
    op.drop_table('topology_links')
    op.drop_table('neighbors')
