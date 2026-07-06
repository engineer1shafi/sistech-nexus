from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.entity import Entity


class SNMPProfile(Entity):
    __tablename__ = "snmp_profiles"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    version: Mapped[str] = mapped_column(String(10), default="v2c", nullable=False)
    community: Mapped[str | None] = mapped_column(String(255), nullable=True)

    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    auth_protocol: Mapped[str | None] = mapped_column(String(50), nullable=True)
    auth_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    priv_protocol: Mapped[str | None] = mapped_column(String(50), nullable=True)
    priv_password: Mapped[str | None] = mapped_column(String(255), nullable=True)

    port: Mapped[int] = mapped_column(Integer, default=161, nullable=False)
    timeout: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    retries: Mapped[int] = mapped_column(Integer, default=2, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)