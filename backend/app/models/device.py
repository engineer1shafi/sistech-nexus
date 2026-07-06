from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.entity import Entity


class Device(Entity):
    __tablename__ = "devices"

    organization_id: Mapped[str] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    site_id: Mapped[str | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("sites.id"),
        nullable=True,
        index=True,
    )

    vendor_id: Mapped[str | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("vendors.id"),
        nullable=True,
        index=True,
    )

    device_type_id: Mapped[str | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("device_types.id"),
        nullable=True,
        index=True,
    )

    snmp_profile_id: Mapped[str | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("snmp_profiles.id"),
        nullable=True,
        index=True,
    )

    hostname: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    ip_address: Mapped[str] = mapped_column(String(45), unique=True, nullable=False, index=True)

    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    serial_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    os_version: Mapped[str | None] = mapped_column(String(150), nullable=True)

    status: Mapped[str] = mapped_column(String(30), default="unknown", nullable=False, index=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    organization = relationship("Organization", lazy="selectin")
    site = relationship("Site", lazy="selectin")
    vendor = relationship("Vendor", lazy="selectin")
    device_type = relationship("DeviceType", lazy="selectin")
    snmp_profile = relationship("SNMPProfile", lazy="selectin")