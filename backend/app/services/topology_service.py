from __future__ import annotations

from typing import Any
from uuid import UUID

from app.repositories.topology_repository import TopologyRepository
from app.repositories.neighbor_repository import NeighborRepository


class TopologyService:
    def __init__(self, db):
        self.topology_repo = TopologyRepository(db)
        self.neighbor_repo = NeighborRepository(db)

    async def get_topology(self) -> dict[str, list[Any]]:
        links = await self.topology_repo.list_all()

        nodes: dict[str, dict[str, Any]] = {}
        edge_list: list[dict[str, Any]] = []

        for link in links:
            src = str(link.source_device_id)
            tgt = str(link.target_device_id) if link.target_device_id else None

            nodes.setdefault(src, {"id": src})
            if tgt:
                nodes.setdefault(tgt, {"id": tgt})

            edge_list.append({
                "id": str(link.id),
                "source": src,
                "target": tgt,
                "protocol": link.protocol,
                "confidence": link.confidence,
            })

        return {"nodes": list(nodes.values()), "links": edge_list}

    async def get_device_neighbors(self, device_id: UUID) -> list[dict[str, Any]]:
        neighbors = await self.neighbor_repo.list_by_device(device_id)
        result: list[dict[str, Any]] = []

        for n in neighbors:
            result.append({
                "id": str(n.id),
                "local_device_id": str(n.local_device_id),
                "local_interface_id": str(n.local_interface_id) if n.local_interface_id else None,
                "protocol": n.protocol,
                "remote_chassis_id": n.remote_chassis_id,
                "remote_port_id": n.remote_port_id,
                "remote_system_name": n.remote_system_name,
                "remote_system_description": n.remote_system_description,
                "remote_management_address": n.remote_management_address,
                "remote_capabilities": n.remote_capabilities,
                "is_active": n.is_active,
            })

        return result
