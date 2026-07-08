from __future__ import annotations

import asyncio
from typing import Any

from pysnmp.hlapi.asyncio import (
    CommunityData,
    ContextData,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    get_cmd,
)

from app.snmp.adapter_base import SNMPAdapter
from app.snmp.exceptions import (
    SNMPAuthenticationError,
    SNMPResponseError,
    SNMPTimeoutError,
)
from app.snmp.snmp_result import SNMPResult


class PySNMPAdapter(SNMPAdapter):
    """Concrete adapter built on the existing async pysnmp get command."""

    def __init__(self, host: str | None = None, community: str = "public", port: int = 161, timeout: int = 3, retries: int = 2):
        self.host = host
        self.community = community
        self.port = port
        self.timeout = timeout
        self.retries = retries

    def get(
        self,
        oid: str,
        *,
        host: str,
        community: str = "public",
        port: int = 161,
        timeout: int = 3,
    ) -> SNMPResult:
        return asyncio.run(self._get_async(oid=oid, host=host, community=community, port=port, timeout=timeout))

    async def _get_async(self, *, oid: str, host: str, community: str, port: int, timeout: int) -> SNMPResult:
        try:
            error_indication, error_status, error_index, var_binds = await get_cmd(
                SnmpEngine(),
                CommunityData(community, mpModel=1),
                await UdpTransportTarget.create((host, port), timeout=timeout, retries=2),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
            )
        except Exception as exc:  # pragma: no cover - defensive path
            return SNMPResult(oid=oid, value=None, value_type="unknown", success=False, error=str(exc))

        if error_indication:
            message = str(error_indication)
            if "auth" in message.lower() or "unknownuser" in message.lower():
                raise SNMPAuthenticationError(message)
            raise SNMPTimeoutError(message)

        if error_status:
            raise SNMPResponseError(f"{error_status.prettyPrint()} at {error_index}")

        for _, value in var_binds:
            display_value = None
            if value is None:
                display_value = None
            elif hasattr(value, "prettyPrint"):
                display_value = value.prettyPrint()
            else:
                display_value = str(value)

            return SNMPResult(
                oid=oid,
                value=display_value,
                value_type=type(value).__name__,
                success=True,
            )

        return SNMPResult(oid=oid, value=None, value_type="unknown", success=False, error="No value returned")

    def walk(
        self,
        base_oid: str,
        *,
        host: str,
        community: str = "public",
        port: int = 161,
        timeout: int = 3,
    ) -> list[SNMPResult]:
        results: list[SNMPResult] = []
        for index in range(1, 51):
            try:
                result = self.get(f"{base_oid}.{index}", host=host, community=community, port=port, timeout=timeout)
            except Exception:
                continue
            if result.success:
                results.append(result)
        return results

    def bulk_walk(
        self,
        base_oid: str,
        *,
        host: str,
        community: str = "public",
        port: int = 161,
        timeout: int = 3,
        max_repetitions: int = 10,
    ) -> list[SNMPResult]:
        return self.walk(base_oid, host=host, community=community, port=port, timeout=timeout)
