from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class InterfaceMetricResponse(BaseModel):
    id: UUID
    device_id: UUID
    interface_id: UUID
    timestamp: datetime
    admin_status: str | None = None
    oper_status: str | None = None
    rx_octets: int | None = None
    tx_octets: int | None = None
    rx_errors: int | None = None
    tx_errors: int | None = None
    rx_discards: int | None = None
    tx_discards: int | None = None
    speed: int | None = None
    utilization_in: float | None = None
    utilization_out: float | None = None

    model_config = {"from_attributes": True}


class InterfaceMetricCreate(BaseModel):
    device_id: UUID
    interface_id: UUID
    timestamp: datetime
    admin_status: str | None = None
    oper_status: str | None = None
    rx_octets: int | None = None
    tx_octets: int | None = None
    rx_errors: int | None = None
    tx_errors: int | None = None
    rx_discards: int | None = None
    tx_discards: int | None = None
    speed: int | None = None
    utilization_in: float | None = None
    utilization_out: float | None = None
