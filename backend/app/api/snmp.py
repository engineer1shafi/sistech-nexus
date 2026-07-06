import asyncio

from fastapi import APIRouter

from app.schemas.snmp import SNMPTestRequest, SNMPTestResponse
from app.snmp.simple_v2c import test_device

router = APIRouter(prefix="/snmp", tags=["SNMP"])


@router.post("/test", response_model=SNMPTestResponse)
async def snmp_test(payload: SNMPTestRequest):
    try:
        result = await asyncio.to_thread(
            test_device,
            str(payload.ip_address),
            payload.community,
            payload.port,
            payload.timeout,
        )

        return SNMPTestResponse(
            status="success",
            ip_address=str(payload.ip_address),
            sys_name=result.get("sys_name"),
            sys_descr=result.get("sys_descr"),
            sys_uptime=result.get("sys_uptime"),
        )

    except Exception as exc:
        return SNMPTestResponse(
            status="failed",
            ip_address=str(payload.ip_address),
            error=str(exc),
        )