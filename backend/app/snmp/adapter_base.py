from __future__ import annotations

from abc import ABC, abstractmethod

from app.snmp.snmp_result import SNMPResult


class SNMPAdapter(ABC):
    """Abstract interface for SNMP operations."""

    @abstractmethod
    def get(
        self,
        oid: str,
        *,
        host: str,
        community: str = "public",
        port: int = 161,
        timeout: int = 3,
    ) -> SNMPResult:
        """Fetch a single OID value."""
        raise NotImplementedError

    @abstractmethod
    def walk(
        self,
        base_oid: str,
        *,
        host: str,
        community: str = "public",
        port: int = 161,
        timeout: int = 3,
    ) -> list[SNMPResult]:
        """Walk a subtree of OIDs."""
        raise NotImplementedError

    @abstractmethod
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
        """Bulk-walk a subtree of OIDs."""
        raise NotImplementedError
