from app.snmp.poller import SNMPPoller
from app.snmp.vendor_detector import detect_vendor


class SNMPDiscovery:
    def __init__(
        self,
        host: str,
        community: str = "public",
        port: int = 161,
        timeout: int = 3,
        retries: int = 2,
    ):
        self.poller = SNMPPoller(
            host=host,
            community=community,
            port=port,
            timeout=timeout,
            retries=retries,
        )

    async def discover(self) -> dict:
        system = await self.poller.poll_system()

        vendor = detect_vendor(
            system.get("sys_descr"),
            system.get("sys_object_id"),
        )

        return {
            "hostname": system.get("sys_name"),
            "vendor": vendor,
            "sys_descr": system.get("sys_descr"),
            "sys_object_id": system.get("sys_object_id"),
            "sys_uptime": system.get("sys_uptime"),
            "sys_contact": system.get("sys_contact"),
            "sys_location": system.get("sys_location"),
        }