from uuid import UUID

from pydantic import BaseModel


class InterfaceResponse(BaseModel):
    id: UUID
    device_id: UUID
    if_index: int
    if_name: str | None = None
    if_alias: str | None = None
    if_descr: str | None = None
    mac_address: str | None = None
    speed: int | None = None
    mtu: int | None = None
    admin_status: str | None = None
    oper_status: str | None = None
    rx_octets: int | None = None
    tx_octets: int | None = None
    rx_errors: int | None = None
    tx_errors: int | None = None

    model_config = {
        "from_attributes": True
    }