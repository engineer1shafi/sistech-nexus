from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interface import Interface


class InterfaceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_device(self, device_id: UUID) -> list[Interface]:
        result = await self.db.execute(
            select(Interface).where(
                Interface.device_id == device_id,
                Interface.is_deleted == False,
            ).order_by(Interface.if_index)
        )
        return list(result.scalars().all())

    async def get_by_device_and_ifindex(self, device_id: UUID, if_index: int) -> Interface | None:
        result = await self.db.execute(
            select(Interface).where(
                Interface.device_id == device_id,
                Interface.if_index == if_index,
                Interface.is_deleted == False,
            )
        )
        return result.scalar_one_or_none()

    async def create_interface(self, device_id: UUID, data: dict) -> Interface:
        interface = Interface(device_id=device_id, **data)
        self.db.add(interface)
        await self.db.flush()
        return interface

    async def update_interface(self, interface: Interface, data: dict) -> Interface:
        for key, value in data.items():
            setattr(interface, key, value)
        await self.db.flush()
        return interface