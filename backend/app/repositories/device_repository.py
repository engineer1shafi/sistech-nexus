from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.device import Device
from app.models.device_type import DeviceType
from app.models.snmp_profile import SNMPProfile
from app.models.vendor import Vendor
from app.schemas.device import DeviceCreate, DeviceUpdate


class DeviceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_vendor(self, name: str | None) -> Vendor | None:
        if not name:
            return None

        result = await self.db.execute(select(Vendor).where(Vendor.name == name))
        return result.scalar_one_or_none()

    async def _get_device_type(self, name: str | None) -> DeviceType | None:
        if not name:
            return None

        result = await self.db.execute(select(DeviceType).where(DeviceType.name == name))
        return result.scalar_one_or_none()

    async def _get_snmp_profile(self, version: str | None) -> SNMPProfile | None:
        result = await self.db.execute(
            select(SNMPProfile).where(SNMPProfile.name == "Default SNMP v2c")
        )
        return result.scalar_one_or_none()

    async def create(self, payload: DeviceCreate) -> Device:
        vendor = await self._get_vendor(payload.vendor)
        device_type = await self._get_device_type(payload.device_type)
        snmp_profile = await self._get_snmp_profile(payload.snmp_version)

        device = Device(
            organization_id=payload.organization_id,
            hostname=payload.hostname,
            ip_address=str(payload.ip_address),
            vendor_id=vendor.id if vendor else None,
            device_type_id=device_type.id if device_type else None,
            snmp_profile_id=snmp_profile.id if snmp_profile else None,
            model=payload.model,
            serial_number=payload.serial_number,
            status="unknown",
            is_enabled=True,
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