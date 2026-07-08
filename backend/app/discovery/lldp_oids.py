from __future__ import annotations

LLDP_OIDS: dict[str, str] = {
    "lldpRemChassisIdSubtype": "1.0.8802.1.1.2.1.4.1.1.4",
    "lldpRemChassisId": "1.0.8802.1.1.2.1.4.1.1.5",
    "lldpRemPortIdSubtype": "1.0.8802.1.1.2.1.4.1.1.6",
    "lldpRemPortId": "1.0.8802.1.1.2.1.4.1.1.7",
    "lldpRemPortDesc": "1.0.8802.1.1.2.1.4.1.1.8",
    "lldpRemSysName": "1.0.8802.1.1.2.1.4.1.1.9",
    "lldpRemSysDesc": "1.0.8802.1.1.2.1.4.1.1.10",
    "lldpRemSysCapSupported": "1.0.8802.1.1.2.1.4.1.1.11",
    "lldpRemSysCapEnabled": "1.0.8802.1.1.2.1.4.1.1.12",
    "lldpRemManAddr": "1.0.8802.1.1.2.1.4.2.1.4",
}
