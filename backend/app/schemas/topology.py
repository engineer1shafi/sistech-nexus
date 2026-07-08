from __future__ import annotations

from pydantic import BaseModel
from uuid import UUID


class TopologyLinkResponse(BaseModel):
    id: UUID
    source_device_id: UUID
    source_interface_id: UUID | None = None
    target_device_id: UUID | None = None
    target_interface_id: UUID | None = None
    protocol: str
    confidence: int
    is_active: bool

    model_config = {"from_attributes": True}
