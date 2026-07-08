from __future__ import annotations

from typing import Any


def parse_lldp_walk_results(results: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Placeholder parser for LLDP walk results.

    For this foundation commit it accepts a dict of OID name -> list of varbind dicts
    and returns a list of neighbor dicts. Real parsing will map indices and
    perform more robust conversions.
    """
    neighbors: list[dict[str, Any]] = []

    # Foundation: return empty list if no results
    if not results:
        return neighbors

    # Minimal mapping: iterate over one of the lists and build simple entries
    sample_key = next(iter(results.keys()))
    sample_list = results.get(sample_key, [])

    for idx, _ in enumerate(sample_list):
        neighbors.append({
            "remote_chassis_id": None,
            "remote_port_id": None,
            "remote_system_name": None,
            "remote_system_description": None,
            "remote_management_address": None,
            "remote_capabilities": None,
            "protocol": "LLDP",
        })

    return neighbors
