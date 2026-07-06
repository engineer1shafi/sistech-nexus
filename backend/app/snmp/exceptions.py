class SNMPError(Exception):
    pass


class SNMPTimeoutError(SNMPError):
    pass


class SNMPAuthenticationError(SNMPError):
    pass


class SNMPResponseError(SNMPError):
    pass