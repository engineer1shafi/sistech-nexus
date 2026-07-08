from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.device import DeviceCreate, DeviceResponse, DeviceUpdate
from app.services.device_service import DeviceService

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post("", response_model=DeviceResponse)
async def create_device(
    payload: DeviceCreate,
    db: AsyncSession = Depends(get_db),
):
    service = DeviceService(db)
    return await service.create_device(payload)


@router.get("", response_model=list[DeviceResponse])
async def list_devices(
    db: AsyncSession = Depends(get_db),
):
    service = DeviceService(db)
    return await service.list_devices()


@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = DeviceService(db)
    return await service.get_device(device_id)


@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(
    device_id: UUID,
    payload: DeviceUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = DeviceService(db)
    return await service.update_device(device_id, payload)


@router.delete("/{device_id}")
async def delete_device(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = DeviceService(db)
    return await service.delete_device(device_id)


@router.post("/{device_id}/snmp-test")
async def snmp_test_device(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = DeviceService(db)
    return await service.snmp_test_device(device_id)


@router.post("/{device_id}/discover")
async def discover_device(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = DeviceService(db)
    return await service.discover_device(device_id)


@router.post("/{device_id}/discover/interfaces")
async def discover_interfaces(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = DeviceService(db)
    return await service.discover_interfaces(device_id)


@router.post("/{device_id}/discover/lldp")
async def discover_lldp(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = DeviceService(db)
    return await service.discover_lldp(device_id)