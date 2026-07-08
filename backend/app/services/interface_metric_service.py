from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interface_metric_repository import InterfaceMetricRepository


class InterfaceMetricService:
    def __init__(self, db: AsyncSession):
        self.repo = InterfaceMetricRepository(db)

    async def list_interface_metrics(self, interface_id: UUID, limit: int = 100, latest_only: bool = False) -> list[Any]:
        return await self.repo.list_by_interface(interface_id, limit=limit, latest_only=latest_only)

    async def list_device_interface_metrics(self, device_id: UUID, limit: int = 100) -> list[Any]:
        return await self.repo.list_by_device(device_id, limit=limit)

    async def create_metric(self, payload: dict) -> Any:
        return await self.repo.create(payload)
