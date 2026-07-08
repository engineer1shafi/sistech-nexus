from uuid import UUID

from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.entity import Entity


class Interface(Entity):
    __tablename__ = "interfaces"

    device_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    if_index: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    if_name: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    if_alias: Mapped[str | None] = mapped_column(String(255), nullable=True)
    if_descr: Mapped[str | None] = mapped_column(String(255), nullable=True)

    mac_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    speed: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    mtu: Mapped[int | None] = mapped_column(Integer, nullable=True)

    admin_status: Mapped[str | None] = mapped_column(String(30), nullable=True, index=True)
    oper_status: Mapped[str | None] = mapped_column(String(30), nullable=True, index=True)

    rx_octets: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    tx_octets: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    rx_errors: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    tx_errors: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    device = relationship("Device", lazy="selectin")