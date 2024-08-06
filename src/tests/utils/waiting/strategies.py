import asyncio
import time
from abc import ABC, abstractmethod

from tests.utils.waiting.conditions import WaitCondition
from tests.utils.waiting.errors import GivenUpError


class WaitStrategy(ABC):
    """Base class for wait strategies."""

    @abstractmethod
    async def wait(self, condition: WaitCondition) -> None:
        """Wait for condition to be met."""

        pass


class MaxRetriesStrategy(WaitStrategy):
    """Wait strategy that retries a given number of times."""

    def __init__(self, retries: int, interval: float = 1) -> None:
        self._retries = retries
        self._interval = interval

    async def wait(self, condition: WaitCondition) -> None:
        exceptions = []

        for _ in range(self._retries):
            try:
                await condition.check()
            except Exception as ex:
                exceptions.append(ex)
            else:
                return

            await asyncio.sleep(self._interval)

        exception = GivenUpError()

        if exceptions:
            raise exception from exceptions[-1]

        raise exception


class TimeoutStrategy(WaitStrategy):
    """Wait strategy that times out after a given number of seconds."""

    def __init__(self, timeout: float, interval: float = 1) -> None:
        self._timeout = timeout
        self._interval = interval

    def _get_current_time(self) -> float:
        return time.monotonic()

    async def wait(self, condition: WaitCondition) -> None:
        exceptions = []
        start = self._get_current_time()

        while self._get_current_time() - start < self._timeout:
            try:
                await condition.check()
            except Exception as ex:
                exceptions.append(ex)
            else:
                return

            await asyncio.sleep(self._interval)

        exception = GivenUpError()

        if exceptions:
            raise exception from exceptions[-1]

        raise exception
