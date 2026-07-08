from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interface import Interface


class InterfaceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_device(self, device_id: UUID) -> list[Interface]:
        result = await self.db.execute(
            select(Interface).where(
                Interface.device_id == device_id,
                Interface.is_deleted == False,
            ).order_by(Interface.if_index)
        )
        return list(result.scalars().all())