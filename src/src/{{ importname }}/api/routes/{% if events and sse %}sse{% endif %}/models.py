from collections.abc import AsyncIterator
from dataclasses import dataclass


@dataclass(kw_only=True)
class SubscribeRequest:
    """Request to subscribe."""

    pass


@dataclass(kw_only=True)
class SubscribeResponse:
    """Response for subscribe."""

    messages: AsyncIterator[str]
