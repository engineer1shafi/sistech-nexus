from __future__ import annotations

from typing import Any

from app.snmp.snmp_result import SNMPResult


def parse_ifmib_results(results_by_field: dict[str, list[SNMPResult]]) -> list[dict[str, Any]]:
    """Parse collections of SNMP walk results into interface dictionaries."""

    interfaces: dict[int, dict[str, Any]] = {}

    for field_name, results in results_by_field.items():
        for result in results:
            if not result.success or result.value is None:
                continue

            if_index = _extract_if_index(result.oid)
            if if_index is None:
                continue

            entry = interfaces.setdefault(if_index, {"if_index": if_index})

            if field_name == "ifIndex":
                try:
                    entry["if_index"] = int(result.value)
                except (TypeError, ValueError):
                    entry["if_index"] = if_index
            elif field_name == "ifName":
                entry["if_name"] = str(result.value)
            elif field_name == "ifDescr":
                entry["if_descr"] = str(result.value)
            elif field_name == "ifAlias":
                entry["if_alias"] = str(result.value)
            elif field_name == "ifSpeed":
                try:
                    entry["speed"] = int(str(result.value))
                except (TypeError, ValueError):
                    entry["speed"] = None
            elif field_name == "ifMtu":
                try:
                    entry["mtu"] = int(str(result.value))
                except (TypeError, ValueError):
                    entry["mtu"] = None
            elif field_name == "ifAdminStatus":
                entry["admin_status"] = str(result.value)
            elif field_name == "ifOperStatus":
                entry["oper_status"] = str(result.value)
            elif field_name == "ifPhysAddress":
                entry["mac_address"] = str(result.value)

    return list(interfaces.values())


def _extract_if_index(oid: str) -> int | None:
    parts = oid.split(".")
    if not parts:
        return None

    last_part = parts[-1]
    if not last_part.isdigit():
        return None

    return int(last_part)
