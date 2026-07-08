from pydantic import BaseModel, IPvAnyAddress


class SNMPTestRequest(BaseModel):
    ip_address: IPvAnyAddress
    community: str = "public"
    port: int = 161
    timeout: int = 3


class SNMPWalkRequest(BaseModel):
    ip_address: IPvAnyAddress
    community: str = "public"
    port: int = 161
    timeout: int = 3
    oid: str
    limit: int | None = None


class SNMPWalkResult(BaseModel):
    oid: str
    value: str | None = None


class SNMPSystemResponse(BaseModel):
    status: str
    ip_address: str
    sys_name: str | None = None
    sys_descr: str | None = None
    sys_object_id: str | None = None
    sys_uptime: str | None = None
    sys_contact: str | None = None
    sys_location: str | None = None
    error: str | None = None


class SNMPWalkResponse(BaseModel):
    status: str
    ip_address: str
    oid: str
    results: list[SNMPWalkResult] = []
    error: str | None = None


SNMPTestResponse = SNMPSystemResponse