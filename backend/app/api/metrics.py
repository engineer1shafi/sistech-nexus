from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.interface_metric_service import InterfaceMetricService
from app.schemas.interface_metric import InterfaceMetricResponse

router = APIRouter()


@router.get("/metrics/interfaces/{interface_id}", response_model=list[InterfaceMetricResponse])
async def get_interface_metrics(
    interface_id: UUID,
    limit: int = Query(100, ge=1, le=10000),
    latest_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
):
    svc = InterfaceMetricService(db)
    return await svc.list_interface_metrics(interface_id, limit=limit, latest_only=latest_only)


@router.get("/devices/{device_id}/metrics/interfaces", response_model=list[InterfaceMetricResponse])
async def get_device_interface_metrics(
    device_id: UUID,
    limit: int = Query(100, ge=1, le=10000),
    db: AsyncSession = Depends(get_db),
):
    svc = InterfaceMetricService(db)
    return await svc.list_device_interface_metrics(device_id, limit=limit)
