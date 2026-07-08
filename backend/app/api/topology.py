from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.topology_service import TopologyService
from uuid import UUID

router = APIRouter(prefix="/topology", tags=["Topology"])


@router.get("/links")
async def get_links(db: AsyncSession = Depends(get_db)) -> dict:
    service = TopologyService(db)
    return await service.get_topology()


@router.get("/devices/{device_id}/neighbors")
async def get_device_neighbors(device_id: UUID, db: AsyncSession = Depends(get_db)) -> list[dict]:
    service = TopologyService(db)
    return await service.get_device_neighbors(device_id)
