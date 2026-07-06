from uuid import UUID

from pydantic import BaseModel, IPvAnyAddress


class DeviceCreate(BaseModel):
    organization_id: UUID
    hostname: str
    ip_address: IPvAnyAddress
    vendor: str
    model: str | None = None
    serial_number: str | None = None
    device_type: str
    snmp_version: str = "v2c"
    snmp_port: int = 161


class DeviceUpdate(BaseModel):
    hostname: str | None = None
    vendor: str | None = None
    model: str | None = None
    serial_number: str | None = None
    device_type: str | None = None
    snmp_version: str | None = None
    snmp_port: int | None = None
    is_enabled: bool | None = None


class DeviceResponse(BaseModel):
    id: UUID
    organization_id: UUID
    hostname: str
    ip_address: str
    vendor: str
    model: str | None
    serial_number: str | None
    device_type: str
    snmp_version: str
    snmp_port: int
    is_enabled: bool

    model_config = {
        "from_attributes": True
    }