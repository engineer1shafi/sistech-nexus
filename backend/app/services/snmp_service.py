from app.schemas.snmp import (
    SNMPSystemResponse,
    SNMPTestRequest,
    SNMPWalkRequest,
    SNMPWalkResponse,
    SNMPWalkResult,
)
from app.snmp.oids import SYSTEM_OIDS
from app.snmp.poller import SNMPPoller
from app.snmp.simple_v2c import snmp_get


class SNMPService:
    async def test_system(self, payload: SNMPTestRequest) -> SNMPSystemResponse:
        try:
            data = {}
            for key, oid in SYSTEM_OIDS.items():
                data[key] = await self._get_system_value(payload, oid)

            return SNMPSystemResponse(
                status="success",
                ip_address=str(payload.ip_address),
                **data,
            )
        except Exception as exc:
            return SNMPSystemResponse(
                status="failed",
                ip_address=str(payload.ip_address),
                error=str(exc),
            )

    async def walk(self, payload: SNMPWalkRequest) -> SNMPWalkResponse:
        try:
            poller = SNMPPoller(
                host=str(payload.ip_address),
                community=payload.community,
                port=payload.port,
                timeout=payload.timeout,
            )
            results = await poller.walk_subtree(payload.oid, limit=payload.limit)

            return SNMPWalkResponse(
                status="success",
                ip_address=str(payload.ip_address),
                oid=payload.oid,
                results=[SNMPWalkResult(**item) for item in results],
            )
        except Exception as exc:
            return SNMPWalkResponse(
                status="failed",
                ip_address=str(payload.ip_address),
                oid=payload.oid,
                error=str(exc),
            )

    async def _get_system_value(self, payload: SNMPTestRequest, oid: str):
        import asyncio

        return await asyncio.to_thread(
            snmp_get,
            str(payload.ip_address),
            payload.community,
            oid,
            payload.port,
            payload.timeout,
        )
