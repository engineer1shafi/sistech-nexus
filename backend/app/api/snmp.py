from fastapi import APIRouter

from app.schemas.snmp import (
    SNMPSystemResponse,
    SNMPTestRequest,
    SNMPWalkRequest,
    SNMPWalkResponse,
    SNMPWalkResult,
)
from app.services.snmp_service import SNMPService

router = APIRouter(prefix="/snmp", tags=["SNMP"])
service = SNMPService()


@router.post("/test", response_model=SNMPSystemResponse)
async def snmp_test(payload: SNMPTestRequest):
    return await service.test_system(payload)


@router.post("/system", response_model=SNMPSystemResponse)
async def snmp_system(payload: SNMPTestRequest):
    return await service.test_system(payload)


@router.post("/walk", response_model=SNMPWalkResponse)
async def snmp_walk(payload: SNMPWalkRequest):
    return await service.walk(payload)