from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseEntity


class TopologyLink(BaseEntity):
    __tablename__ = "topology_links"

    source_device_id: Mapped[str] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("devices.id", ondelete="CASCADE"), nullable=False, index=True
    )

    source_interface_id: Mapped[str | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("interfaces.id", ondelete="SET NULL"), nullable=True, index=True
    )

    target_device_id: Mapped[str | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("devices.id", ondelete="SET NULL"), nullable=True, index=True
    )

    target_interface_id: Mapped[str | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("interfaces.id", ondelete="SET NULL"), nullable=True, index=True
    )

    protocol: Mapped[str] = mapped_column(String(30), nullable=False, default="LLDP")
    confidence: Mapped[int] = mapped_column(Integer, nullable=False, default=50)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)

    source_device = relationship("Device", lazy="selectin", foreign_keys=[source_device_id])
    target_device = relationship("Device", lazy="selectin", foreign_keys=[target_device_id])
