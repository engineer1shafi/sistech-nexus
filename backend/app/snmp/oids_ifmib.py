from __future__ import annotations

IF_MIB_OIDS: dict[str, str] = {
    "ifDescr": "1.3.6.1.2.1.2.2.1.2",
    "ifType": "1.3.6.1.2.1.2.2.1.3",
    "ifMtu": "1.3.6.1.2.1.2.2.1.4",
    "ifSpeed": "1.3.6.1.2.1.2.2.1.5",
    "ifPhysAddress": "1.3.6.1.2.1.2.2.1.6",
    "ifAdminStatus": "1.3.6.1.2.1.2.2.1.7",
    "ifOperStatus": "1.3.6.1.2.1.2.2.1.8",
    "ifName": "1.3.6.1.2.1.31.1.1.1.1",
    "ifAlias": "1.3.6.1.2.1.31.1.1.1.18",
    "ifHCInOctets": "1.3.6.1.2.1.31.1.1.1.6",
    "ifHCOutOctets": "1.3.6.1.2.1.31.1.1.1.10",
}

IF_DESCR_OID: str = IF_MIB_OIDS["ifDescr"]
IF_TYPE_OID: str = IF_MIB_OIDS["ifType"]
IF_MTU_OID: str = IF_MIB_OIDS["ifMtu"]
IF_SPEED_OID: str = IF_MIB_OIDS["ifSpeed"]
IF_PHYS_ADDRESS_OID: str = IF_MIB_OIDS["ifPhysAddress"]
IF_ADMIN_STATUS_OID: str = IF_MIB_OIDS["ifAdminStatus"]
IF_OPER_STATUS_OID: str = IF_MIB_OIDS["ifOperStatus"]
IF_NAME_OID: str = IF_MIB_OIDS["ifName"]
IF_ALIAS_OID: str = IF_MIB_OIDS["ifAlias"]
IF_HC_IN_OCTETS_OID: str = IF_MIB_OIDS["ifHCInOctets"]
IF_HC_OUT_OCTETS_OID: str = IF_MIB_OIDS["ifHCOutOctets"]
