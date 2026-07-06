from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.entity import Entity


class Permission(Entity):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    roles = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions",
        lazy="selectin",
    )