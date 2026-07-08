class SNMPError(Exception):
    """Base exception for SNMP failures."""


class SNMPTimeoutError(SNMPError):
    """Raised when an SNMP request times out."""


class SNMPAuthenticationError(SNMPError):
    """Raised when SNMP authentication fails."""


class SNMPWalkError(SNMPError):
    """Raised when a walk operation cannot be completed."""


class SNMPResponseError(SNMPError):
    """Raised when an SNMP response is malformed or unexpected."""
