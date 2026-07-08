from __future__ import annotations

from pydantic import BaseModel
from uuid import UUID


class NeighborResponse(BaseModel):
    id: UUID
    local_device_id: UUID
    local_interface_id: UUID | None = None
    protocol: str
    remote_chassis_id: str | None = None
    remote_port_id: str | None = None
    remote_system_name: str | None = None
    remote_system_description: str | None = None
    remote_management_address: str | None = None
    remote_capabilities: str | None = None
    is_active: bool

    model_config = {"from_attributes": True}
