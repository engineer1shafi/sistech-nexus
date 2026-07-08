from __future__ import annotations

from pydantic import BaseModel
from uuid import UUID


class PollingPolicyResponse(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    interval_seconds: int
    timeout_seconds: int
    retries: int
    is_default: bool
    is_active: bool

    model_config = {"from_attributes": True}


class PollingPolicyCreate(BaseModel):
    name: str
    description: str | None = None
    interval_seconds: int | None = None
    timeout_seconds: int | None = None
    retries: int | None = None
    is_default: bool | None = False
    is_active: bool | None = True
