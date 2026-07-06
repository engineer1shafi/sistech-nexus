from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.entity import Entity


class Vendor(Entity):
    __tablename__ = "vendors"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)