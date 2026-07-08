from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.neighbor import Neighbor


class NeighborRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_device(self, device_id: UUID) -> list[Neighbor]:
        result = await self.db.execute(
            select(Neighbor).where(Neighbor.local_device_id == device_id)
        )
        return list(result.scalars().all())

    async def create(self, data: dict) -> Neighbor:
        n = Neighbor(**data)
        self.db.add(n)
        await self.db.flush()
        return n

    async def update(self, neighbor: Neighbor, data: dict) -> Neighbor:
        for k, v in data.items():
            setattr(neighbor, k, v)
        await self.db.flush()
        return neighbor
