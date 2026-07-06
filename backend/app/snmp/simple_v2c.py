import random
import socket


OIDS = {
    "sysDescr": "1.3.6.1.2.1.1.1.0",
    "sysUpTime": "1.3.6.1.2.1.1.3.0",
    "sysName": "1.3.6.1.2.1.1.5.0",
}


def _len(data: bytes) -> bytes:
    l = len(data)
    if l < 128:
        return bytes([l])
    b = l.to_bytes((l.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(b)]) + b


def _tlv(tag: int, value: bytes) -> bytes:
    return bytes([tag]) + _len(value) + value


def _int(value: int) -> bytes:
    if value == 0:
        return _tlv(0x02, b"\x00")
    b = value.to_bytes((value.bit_length() + 7) // 8, "big")
    if b[0] & 0x80:
        b = b"\x00" + b
    return _tlv(0x02, b)


def _str(value: str) -> bytes:
    return _tlv(0x04, value.encode())


def _null() -> bytes:
    return b"\x05\x00"


def _oid(oid: str) -> bytes:
    parts = [int(x) for x in oid.split(".")]
    encoded = bytes([40 * parts[0] + parts[1]])

    for part in parts[2:]:
        stack = [part & 0x7F]
        part >>= 7
        while part:
            stack.insert(0, 0x80 | (part & 0x7F))
            part >>= 7
        encoded += bytes(stack)

    return _tlv(0x06, encoded)


def _seq(value: bytes) -> bytes:
    return _tlv(0x30, value)


def _get_request(community: str, oid: str) -> bytes:
    req_id = random.randint(10000, 999999)

    varbind = _seq(_oid(oid) + _null())
    varbind_list = _seq(varbind)

    pdu = _tlv(
        0xA0,
        _int(req_id) + _int(0) + _int(0) + varbind_list,
    )

    return _seq(
        _int(1) + _str(community) + pdu
    )


def _read_len(data: bytes, index: int):
    first = data[index]
    index += 1

    if first < 128:
        return first, index

    count = first & 0x7F
    length = int.from_bytes(data[index:index + count], "big")
    index += count

    return length, index


def _read_tlv(data: bytes, index: int):
    tag = data[index]
    index += 1
    length, index = _read_len(data, index)
    value = data[index:index + length]
    index += length
    return tag, value, index


def _decode_value(tag: int, value: bytes):
    if tag == 0x04:
        return value.decode(errors="ignore")

    if tag in (0x02, 0x41, 0x42, 0x43, 0x46):
        number = int.from_bytes(value, "big")
        if tag == 0x43:
            seconds = number // 100
            return f"{seconds} seconds"
        return str(number)

    if tag == 0x40:
        return ".".join(str(x) for x in value)

    if tag == 0x05:
        return None

    return value.hex()


def _extract_response(data: bytes):
    def walk(buf: bytes):
        index = 0
        values = []

        while index < len(buf):
            tag, value, index = _read_tlv(buf, index)

            if tag in (0x30, 0xA2):
                values.extend(walk(value))
            else:
                values.append((tag, value))

        return values

    values = walk(data)

    for tag, value in reversed(values):
        if tag not in (0x02, 0x04, 0x05, 0x06):
            return _decode_value(tag, value)

    for tag, value in reversed(values):
        if tag == 0x04:
            return _decode_value(tag, value)

    return None


def snmp_get(ip: str, community: str, oid: str, port: int = 161, timeout: int = 3):
    packet = _get_request(community, oid)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        sock.sendto(packet, (ip, port))
        data, _ = sock.recvfrom(65535)

    return _extract_response(data)


def test_device(ip: str, community: str = "public", port: int = 161, timeout: int = 3):
    return {
        "sys_descr": snmp_get(ip, community, OIDS["sysDescr"], port, timeout),
        "sys_uptime": snmp_get(ip, community, OIDS["sysUpTime"], port, timeout),
        "sys_name": snmp_get(ip, community, OIDS["sysName"], port, timeout),
    }