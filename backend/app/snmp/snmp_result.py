from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SNMPResult:
    """Structured representation of an SNMP lookup result."""

    oid: str
    value: Any
    value_type: str
    success: bool
    error: str | None = None
