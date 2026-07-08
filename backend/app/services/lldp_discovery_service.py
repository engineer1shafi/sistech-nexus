from __future__ import annotations

from uuid import UUID
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.discovery.lldp_discovery import LLDPDiscovery


class LLDPDiscoveryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.discovery = LLDPDiscovery(db)

    async def discover_for_device(self, device_id: UUID, host: str, community: str, port: int, timeout: int) -> dict[str, Any]:
        return await self.discovery.discover(device_id=device_id, host=host, community=community, port=port, timeout=timeout)
