from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseEntity


class Neighbor(BaseEntity):
    __tablename__ = "neighbors"

    local_device_id: Mapped[str] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("devices.id", ondelete="CASCADE"), nullable=False, index=True
    )

    local_interface_id: Mapped[str | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("interfaces.id", ondelete="SET NULL"), nullable=True, index=True
    )

    protocol: Mapped[str] = mapped_column(String(30), nullable=False, default="LLDP")

    remote_chassis_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    remote_port_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    remote_system_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    remote_system_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    remote_management_address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    remote_capabilities: Mapped[str | None] = mapped_column(String(255), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)

    local_device = relationship("Device", lazy="selectin")
    local_interface = relationship("Interface", lazy="selectin")
