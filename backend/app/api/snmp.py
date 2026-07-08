import asyncio

from fastapi import APIRouter

from app.schemas.snmp import SNMPSystemResponse, SNMPTestRequest
from app.snmp.oids import SYSTEM_OIDS
from app.snmp.simple_v2c import snmp_get

router = APIRouter(prefix="/snmp", tags=["SNMP"])


async def get_system_info(payload: SNMPTestRequest) -> dict:
    data = {}

    for key, oid in SYSTEM_OIDS.items():
        data[key] = await asyncio.to_thread(
            snmp_get,
            str(payload.ip_address),
            payload.community,
            oid,
            payload.port,
            payload.timeout,
        )

    return data


@router.post("/test", response_model=SNMPSystemResponse)
async def snmp_test(payload: SNMPTestRequest):
    try:
        result = await get_system_info(payload)

        return SNMPSystemResponse(
            status="success",
            ip_address=str(payload.ip_address),
            **result,
        )

    except Exception as exc:
        return SNMPSystemResponse(
            status="failed",
            ip_address=str(payload.ip_address),
            error=str(exc),
        )


@router.post("/system", response_model=SNMPSystemResponse)
async def snmp_system(payload: SNMPTestRequest):
    return await snmp_test(payload)