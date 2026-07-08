from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interface_repository import InterfaceRepository


class InterfaceService:
    def __init__(self, db: AsyncSession):
        self.repository = InterfaceRepository(db)

    async def list_device_interfaces(self, device_id: UUID):
        return await self.repository.list_by_device(device_id)