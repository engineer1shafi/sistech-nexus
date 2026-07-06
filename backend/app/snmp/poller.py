from app.snmp.client import SNMPClient
from app.snmp.oids import STANDARD_SYSTEM_OIDS


class SNMPPoller:
    def __init__(
        self,
        host: str,
        community: str = "public",
        port: int = 161,
        timeout: int = 3,
        retries: int = 2,
    ):
        self.client = SNMPClient(
            host=host,
            community=community,
            port=port,
            timeout=timeout,
            retries=retries,
        )

    async def poll_system(self) -> dict:
        result = {}

        for name, oid in STANDARD_SYSTEM_OIDS.items():
            try:
                result[name] = await self.client.get(oid)
            except Exception as exc:
                result[name] = None
                result[f"{name}_error"] = str(exc)

        return result