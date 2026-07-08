from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.device import Device
from app.repositories.device_repository import DeviceRepository
from app.schemas.device import DeviceCreate, DeviceResponse, DeviceUpdate
from app.discovery.interface_discovery import InterfaceDiscoveryService
from app.services.lldp_discovery_service import LLDPDiscoveryService
from app.repositories.interface_repository import InterfaceRepository
from app.snmp.simple_v2c import snmp_get
from time import perf_counter


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

    async def delete_device(self, device_id: UUID) -> dict:
        device = await self.repository.get_by_id(device_id)

        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found",
            )

        await self.repository.soft_delete(device)

        return {"message": "Device deleted successfully"}

    async def snmp_test_device(self, device_id: UUID) -> dict:
        device = await self.repository.get_by_id(device_id)

        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found",
            )

        if not device.snmp_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SNMP profile not assigned to this device",
            )

        from app.snmp.simple_v2c import test_device

        result = test_device(
            ip=device.ip_address,
            community=device.snmp_profile.community or "public",
            port=device.snmp_profile.port,
            timeout=device.snmp_profile.timeout,
        )

        return {
            "device_id": str(device.id),
            "hostname": device.hostname,
            "ip_address": device.ip_address,
            "status": "success",
            **result,
        }

    async def discover_device(self, device_id: UUID) -> dict:
        device = await self.repository.get_by_id(device_id)

        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found",
            )

        return {
            "device_id": str(device.id),
            "hostname": device.hostname,
            "ip_address": device.ip_address,
            "message": "Discovery endpoint ready. Interface discovery will be added in next commit.",
        }

    async def discover_interfaces(self, device_id: UUID) -> dict:
        device = await self.repository.get_by_id(device_id)

        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found",
            )

        if not device.snmp_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SNMP profile not assigned to this device",
            )

        service = InterfaceDiscoveryService(self.repository.db, None)
        return await service.discover_interfaces(
            device_id=device.id,
            host=device.ip_address,
            community=device.snmp_profile.community or "public",
            port=device.snmp_profile.port,
            timeout=device.snmp_profile.timeout,
        )

    async def discover_lldp(self, device_id: UUID) -> dict:
        device = await self.repository.get_by_id(device_id)

        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found",
            )

        if not device.snmp_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SNMP profile not assigned to this device",
            )

        service = LLDPDiscoveryService(self.repository.db)
        return await service.discover_for_device(
            device_id=device.id,
            host=device.ip_address,
            community=device.snmp_profile.community or "public",
            port=device.snmp_profile.port,
            timeout=device.snmp_profile.timeout,
        )

    async def poll_device(self, device_id: UUID) -> dict:
        device = await self.repository.get_by_id(device_id)

        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found",
            )

        if not device.snmp_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SNMP profile not assigned to this device",
            )

        community = device.snmp_profile.community or "public"
        port = device.snmp_profile.port
        timeout = device.snmp_profile.timeout

        # perform a simple SNMP get for sysUpTime and measure response time
        start = perf_counter()
        try:
            sys_uptime = snmp_get(device.ip_address, community, "1.3.6.1.2.1.1.3.0", port, timeout)
            response_ms = int((perf_counter() - start) * 1000)
            status_text = "success"
        except Exception as e:
            sys_uptime = None
            response_ms = None
            status_text = "error"

        # interface summary from repository
        iface_repo = InterfaceRepository(self.repository.db)
        interfaces = await iface_repo.list_by_device(device.id)

        interfaces_summary = [
            {
                "id": str(i.id),
                "if_index": i.if_index,
                "if_name": i.if_name,
                "admin_status": i.admin_status,
                "oper_status": i.oper_status,
                "rx_octets": i.rx_octets,
                "tx_octets": i.tx_octets,
            }
            for i in interfaces
        ]

        return {
            "device_id": str(device.id),
            "hostname": device.hostname,
            "ip_address": device.ip_address,
            "status": status_text,
            "response_time_ms": response_ms,
            "sys_uptime": sys_uptime,
            "cpu": None,
            "memory": None,
            "interfaces": interfaces_summary,
        }