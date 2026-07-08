from pysnmp.hlapi.asyncio import (
    CommunityData,
    ContextData,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    get_cmd,
    nextCmd,
)

from app.snmp.exceptions import SNMPResponseError, SNMPTimeoutError


def normalize_var_binds(var_binds: list[tuple]) -> list[dict[str, str | None]]:
    normalized: list[dict[str, str | None]] = []

    for oid, value in var_binds:
        display_value = None

        if value is None:
            display_value = None
        elif hasattr(value, "prettyPrint"):
            display_value = value.prettyPrint()
        else:
            display_value = str(value)

        normalized.append({
            "oid": str(oid),
            "value": display_value,
        })

    return normalized


class SNMPClient:
    def __init__(
        self,
        host: str,
        community: str = "public",
        port: int = 161,
        timeout: int = 3,
        retries: int = 2,
    ):
        self.host = host
        self.community = community
        self.port = port
        self.timeout = timeout
        self.retries = retries

    async def get(self, oid: str) -> str | None:
        error_indication, error_status, error_index, var_binds = await get_cmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            await UdpTransportTarget.create(
                (self.host, self.port),
                timeout=self.timeout,
                retries=self.retries,
            ),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
        )

        if error_indication:
            raise SNMPTimeoutError(str(error_indication))

        if error_status:
            raise SNMPResponseError(
                f"{error_status.prettyPrint()} at {error_index}"
            )

        for _, value in var_binds:
            return value.prettyPrint()

        return None

    async def walk(
        self,
        oid: str,
        limit: int | None = None,
    ) -> list[dict[str, str | None]]:
        error_indication, error_status, error_index, var_binds = await nextCmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            await UdpTransportTarget.create(
                (self.host, self.port),
                timeout=self.timeout,
                retries=self.retries,
            ),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False,
        )

        if error_indication:
            raise SNMPTimeoutError(str(error_indication))

        if error_status:
            raise SNMPResponseError(
                f"{error_status.prettyPrint()} at {error_index}"
            )

        normalized = normalize_var_binds(var_binds)

        if limit is not None:
            return normalized[:limit]

        return normalized