from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.device import Device
from app.repositories.device_repository import DeviceRepository
from app.schemas.device import DeviceCreate, DeviceResponse, DeviceUpdate


class DeviceService:
    def __init__(self, db: AsyncSession):
        self.repository = DeviceRepository(db)

    def _to_response(self, device: Device) -> DeviceResponse:
        return DeviceResponse(
            id=device.id,
            organization_id=device.organization_id,
            hostname=device.hostname,
            ip_address=device.ip_address,
            model=device.model,
            serial_number=device.serial_number,
            os_version=device.os_version,
            status=device.status,
            is_enabled=device.is_enabled,
            vendor=device.vendor.name if device.vendor else None,
            device_type=device.device_type.name if device.device_type else None,
            snmp_version=device.snmp_profile.version if device.snmp_profile else None,
            snmp_port=device.snmp_profile.port if device.snmp_profile else None,
        )

    async def create_device(self, payload: DeviceCreate) -> DeviceResponse:
        device = await self.repository.create(payload)
        return self._to_response(device)

    async def list_devices(self) -> list[DeviceResponse]:
        devices = await self.repository.list_all()
        return [self._to_response(device) for device in devices]

    async def get_device(self, device_id: UUID) -> DeviceResponse:
        device = await self.repository.get_by_id(device_id)

        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found",
            )

        return self._to_response(device)

    async def update_device(self, device_id: UUID, payload: DeviceUpdate) -> DeviceResponse:
        device = await self.repository.get_by_id(device_id)

        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found",
            )

        updated = await self.repository.update(device, payload)
        return self._to_response(updated)

    async def delete_device(self, device_id: UUID):
        device = await self.repository.get_by_id(device_id)

        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found",
            )

        await self.repository.soft_delete(device)

        return {
            "message": "Device deleted successfully"
        }