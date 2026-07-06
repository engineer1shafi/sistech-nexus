from enum import StrEnum


class VendorName(StrEnum):
    HUAWEI = "Huawei"
    CISCO = "Cisco"
    MIKROTIK = "MikroTik"
    FORTINET = "Fortinet"
    JUNIPER = "Juniper"
    HP_ARUBA = "HP/Aruba"
    DELL = "Dell"
    UNKNOWN = "Unknown"


def detect_vendor(sys_descr: str | None, sys_object_id: str | None) -> str:
    text = f"{sys_descr or ''} {sys_object_id or ''}".lower()

    if "huawei" in text or "1.3.6.1.4.1.2011" in text:
        return VendorName.HUAWEI

    if "cisco" in text or "1.3.6.1.4.1.9" in text:
        return VendorName.CISCO

    if "mikrotik" in text or "routeros" in text or "1.3.6.1.4.1.14988" in text:
        return VendorName.MIKROTIK

    if "fortinet" in text or "fortigate" in text or "1.3.6.1.4.1.12356" in text:
        return VendorName.FORTINET

    if "juniper" in text or "junos" in text or "1.3.6.1.4.1.2636" in text:
        return VendorName.JUNIPER

    if "aruba" in text or "procurve" in text or "hewlett" in text:
        return VendorName.HP_ARUBA

    if "dell" in text or "powerconnect" in text:
        return VendorName.DELL

    return VendorName.UNKNOWN