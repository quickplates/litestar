from dataclasses import dataclass


@dataclass(kw_only=True)
class PingRequest:
    """Request to ping."""

    pass


@dataclass(kw_only=True)
class PingResponse:
    """Response for ping."""

    pass
