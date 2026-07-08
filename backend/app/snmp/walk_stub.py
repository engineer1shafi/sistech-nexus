from __future__ import annotations

from app.snmp.adapter_base import SNMPAdapter
from app.snmp.snmp_result import SNMPResult


class SimpleSNMPWalkAdapter(SNMPAdapter):
    """Safe placeholder adapter for future walk-style SNMP support.

    The current implementation intentionally raises NotImplementedError for the walk
    operations so the existing SNMP APIs remain unchanged while the adapter is
    implemented incrementally.
    """

    def get(
        self,
        oid: str,
        *,
        host: str,
        community: str = "public",
        port: int = 161,
        timeout: int = 3,
    ) -> SNMPResult:
        raise NotImplementedError("SimpleSNMPWalkAdapter.get is not implemented yet")

    def walk(
        self,
        base_oid: str,
        *,
        host: str,
        community: str = "public",
        port: int = 161,
        timeout: int = 3,
    ) -> list[SNMPResult]:
        raise NotImplementedError("SimpleSNMPWalkAdapter.walk is not implemented yet")

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
        raise NotImplementedError("SimpleSNMPWalkAdapter.bulk_walk is not implemented yet")
