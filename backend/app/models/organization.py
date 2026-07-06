from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.entity import Entity


class Organization(Entity):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    users = relationship("User", back_populates="organization", lazy="selectin")