from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


class DeviceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload: DeviceCreate) -> Device:
        device = Device(
            organization_id=payload.organization_id,
            hostname=payload.hostname,
            ip_address=str(payload.ip_address),
            vendor=payload.vendor,
            model=payload.model,
            serial_number=payload.serial_number,
            device_type=payload.device_type,
            snmp_version=payload.snmp_version,
            snmp_port=payload.snmp_port,
        )

        self.db.add(device)
        await self.db.commit()
        await self.db.refresh(device)

        return device

    async def list_all(self) -> list[Device]:
        result = await self.db.execute(
            select(Device).where(Device.is_deleted == False)
        )
        return list(result.scalars().all())

    async def get_by_id(self, device_id: UUID) -> Device | None:
        result = await self.db.execute(
            select(Device).where(
                Device.id == device_id,
                Device.is_deleted == False,
            )
        )
        return result.scalar_one_or_none()

    async def update(self, device: Device, payload: DeviceUpdate) -> Device:
        update_data = payload.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(device, key, value)

        await self.db.commit()
        await self.db.refresh(device)

        return device

    async def soft_delete(self, device: Device) -> None:
        device.is_deleted = True
        await self.db.commit()