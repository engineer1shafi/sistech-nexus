from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.polling_policy_service import PollingPolicyService
from app.schemas.polling_policy import PollingPolicyCreate, PollingPolicyResponse

router = APIRouter(prefix="/polling-policies", tags=["Polling Policies"])


@router.get("", response_model=list[PollingPolicyResponse])
async def list_policies(db: AsyncSession = Depends(get_db)):
    service = PollingPolicyService(db)
    return await service.list_policies()


@router.post("", response_model=PollingPolicyResponse)
async def create_policy(payload: PollingPolicyCreate, db: AsyncSession = Depends(get_db)):
    service = PollingPolicyService(db)
    policy = await service.create_policy(payload.model_dump())
    return policy
