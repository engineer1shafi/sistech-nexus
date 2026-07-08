from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.topology_link import TopologyLink


class TopologyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_links_for_device(self, device_id: UUID) -> list[TopologyLink]:
        result = await self.db.execute(
            select(TopologyLink).where(TopologyLink.source_device_id == device_id)
        )
        return list(result.scalars().all())

    async def create(self, data: dict) -> TopologyLink:
        t = TopologyLink(**data)
        self.db.add(t)
        await self.db.flush()
        return t

    async def update(self, link: TopologyLink, data: dict) -> TopologyLink:
        for k, v in data.items():
            setattr(link, k, v)
        await self.db.flush()
        return link
