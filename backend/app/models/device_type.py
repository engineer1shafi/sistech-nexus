from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.entity import Entity


class DeviceType(Entity):
    __tablename__ = "device_types"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)