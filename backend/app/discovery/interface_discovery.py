from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interface_repository import InterfaceRepository
from app.snmp.adapter_base import SNMPAdapter
from app.snmp.snmp_result import SNMPResult
from app.discovery.ifmib_parser import parse_ifmib_results

logger = logging.getLogger(__name__)


class InterfaceDiscoveryService:
    def __init__(self, db: AsyncSession, adapter: SNMPAdapter | None = None):
        self.db = db
        self.repository = InterfaceRepository(db)
        self.adapter = adapter

    async def discover_interfaces(self, device_id: UUID, host: str, community: str, port: int, timeout: int) -> dict[str, Any]:
        if self.adapter is None:
            from app.snmp.adapter_v2c import PySNMPAdapter

            self.adapter = PySNMPAdapter()

        logger.info("Starting interface discovery", extra={"device_id": str(device_id), "host": host})

        fields = [
            ("ifIndex", "1.3.6.1.2.1.2.2.1.1"),
            ("ifName", "1.3.6.1.2.1.31.1.1.1.1"),
            ("ifDescr", "1.3.6.1.2.1.2.2.1.2"),
            ("ifAlias", "1.3.6.1.2.1.31.1.1.1.18"),
            ("ifSpeed", "1.3.6.1.2.1.2.2.1.5"),
            ("ifMtu", "1.3.6.1.2.1.2.2.1.4"),
            ("ifAdminStatus", "1.3.6.1.2.1.2.2.1.7"),
            ("ifOperStatus", "1.3.6.1.2.1.2.2.1.8"),
            ("ifPhysAddress", "1.3.6.1.2.1.2.2.1.6"),
        ]

        results_by_field: dict[str, list[SNMPResult]] = {}
        for field_name, oid in fields:
            try:
                values = await self._run_walk(base_oid=oid, host=host, community=community, port=port, timeout=timeout)
                results_by_field[field_name] = values
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.warning("Interface discovery lookup failed", extra={"oid": oid, "error": str(exc)})
                results_by_field[field_name] = [
                    SNMPResult(
                        oid=oid,
                        value=None,
                        value_type="unknown",
                        success=False,
                        error=str(exc),
                    )
                ]

        parsed_interfaces = parse_ifmib_results(results_by_field)

        created = 0
        updated = 0
        for interface_data in parsed_interfaces:
            existing = await self.repository.get_by_device_and_ifindex(device_id, interface_data["if_index"])
            if existing:
                await self.repository.update_interface(existing, interface_data)
                updated += 1
            else:
                await self.repository.create_interface(device_id, interface_data)
                created += 1

        await self.db.commit()

        logger.info(
            "Finished interface discovery",
            extra={
                "device_id": str(device_id),
                "interfaces_found": len(parsed_interfaces),
                "created": created,
                "updated": updated,
            },
        )

        return {
            "device_id": str(device_id),
            "interfaces_found": len(parsed_interfaces),
            "created": created,
            "updated": updated,
        }

    async def _run_walk(self, *, base_oid: str, host: str, community: str, port: int, timeout: int) -> list[SNMPResult]:
        return await self._call_async(
            self.adapter.walk,
            base_oid=base_oid,
            host=host,
            community=community,
            port=port,
            timeout=timeout,
        )

    async def _call_async(self, func: Any, **kwargs: Any) -> Any:
        import asyncio

        return await asyncio.to_thread(func, **kwargs)
