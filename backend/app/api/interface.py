from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.interface import InterfaceResponse
from app.services.interface_service import InterfaceService

router = APIRouter(tags=["Interfaces"])


@router.get("/devices/{device_id}/interfaces", response_model=list[InterfaceResponse])
async def list_device_interfaces(
    device_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    service = InterfaceService(db)
    return await service.list_device_interfaces(device_id)