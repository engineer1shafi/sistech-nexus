from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.device_repository import DeviceRepository
from app.schemas.device import DeviceCreate, DeviceUpdate


class DeviceService:
    def __init__(self, db: AsyncSession):
        self.repository = DeviceRepository(db)

    async def create_device(self, payload: DeviceCreate):
        return await self.repository.create(payload)

    async def list_devices(self):
        return await self.repository.list_all()

    async def get_device(self, device_id: UUID):
        device = await self.repository.get_by_id(device_id)

        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found",
            )

        return device

    async def update_device(self, device_id: UUID, payload: DeviceUpdate):
        device = await self.get_device(device_id)
        return await self.repository.update(device, payload)

    async def delete_device(self, device_id: UUID):
        device = await self.get_device(device_id)
        await self.repository.soft_delete(device)

        return {
            "message": "Device deleted successfully"
        }