from app.models.base import BaseEntity


class Entity(BaseEntity):
    """
    Base entity for all database models.
    """

    __abstract__ = True