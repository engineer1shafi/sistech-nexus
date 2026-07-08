from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.polling_policy import PollingPolicy


class PollingPolicyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self) -> list[PollingPolicy]:
        result = await self.db.execute(select(PollingPolicy))
        return list(result.scalars().all())

    async def create(self, data: dict) -> PollingPolicy:
        p = PollingPolicy(**data)
        self.db.add(p)
        await self.db.flush()
        return p
