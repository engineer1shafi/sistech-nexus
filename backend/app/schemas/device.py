from uuid import UUID

from pydantic import BaseModel, IPvAnyAddress


class DeviceCreate(BaseModel):
    organization_id: UUID
    hostname: str
    ip_address: IPvAnyAddress
    vendor: str | None = None
    model: str | None = None
    serial_number: str | None = None
    device_type: str | None = None
    snmp_version: str | None = "v2c"
    snmp_port: int | None = 161


class DeviceUpdate(BaseModel):
    hostname: str | None = None
    model: str | None = None
    serial_number: str | None = None
    os_version: str | None = None
    status: str | None = None
    is_enabled: bool | None = None


class DeviceResponse(BaseModel):
    id: UUID
    organization_id: UUID
    hostname: str
    ip_address: str
    model: str | None = None
    serial_number: str | None = None
    os_version: str | None = None
    status: str
    is_enabled: bool

    vendor: str | None = None
    device_type: str | None = None
    snmp_version: str | None = None
    snmp_port: int | None = None

    model_config = {
        "from_attributes": True
    }