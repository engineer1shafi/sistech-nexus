from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interface_metric import InterfaceMetric


class InterfaceMetricRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_interface(self, interface_id: UUID, limit: int = 100, latest_only: bool = False) -> list[InterfaceMetric]:
        q = select(InterfaceMetric).where(InterfaceMetric.interface_id == interface_id)
        q = q.order_by(desc(InterfaceMetric.timestamp))
        if latest_only:
            q = q.limit(1)
        else:
            q = q.limit(limit)

        result = await self.db.execute(q)
        return list(result.scalars().all())

    async def list_by_device(self, device_id: UUID, limit: int = 100) -> list[InterfaceMetric]:
        q = select(InterfaceMetric).where(InterfaceMetric.device_id == device_id).order_by(desc(InterfaceMetric.timestamp)).limit(limit)
        result = await self.db.execute(q)
        return list(result.scalars().all())

    async def create(self, payload: dict) -> InterfaceMetric:
        m = InterfaceMetric(**payload)
        self.db.add(m)
        await self.db.flush()
        return m
