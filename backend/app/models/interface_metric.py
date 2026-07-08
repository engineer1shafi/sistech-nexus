from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.entity import Entity


class InterfaceMetric(Entity):
    __tablename__ = "interface_metrics"
    __table_args__ = (
        Index("ix_interface_metrics_interface_id_timestamp", "interface_id", "timestamp"),
    )

    device_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("devices.id", ondelete="CASCADE"), nullable=False, index=True
    )

    interface_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("interfaces.id", ondelete="CASCADE"), nullable=False, index=True
    )

    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    admin_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    oper_status: Mapped[str | None] = mapped_column(String(30), nullable=True)

    rx_octets: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    tx_octets: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    rx_errors: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    tx_errors: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    rx_discards: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    tx_discards: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    speed: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    utilization_in: Mapped[float | None] = mapped_column(Float, nullable=True)
    utilization_out: Mapped[float | None] = mapped_column(Float, nullable=True)

    device = relationship("Device", lazy="selectin")
    interface = relationship("Interface", lazy="selectin")


Index("ix_interface_metrics_interface_id_timestamp", InterfaceMetric.__tablename__, "interface_id", "timestamp")
