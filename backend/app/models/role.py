from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.entity import Entity


class Role(Entity):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    users = relationship("User", secondary="user_roles", back_populates="roles", lazy="selectin")
    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles",
        lazy="selectin",
    )