from tests.utils.waiting.conditions import WaitCondition
from tests.utils.waiting.strategies import WaitStrategy


class Waiter:
    """Waits for a condition to be met using a given strategy."""

    def __init__(self, condition: WaitCondition, strategy: WaitStrategy) -> None:
        self._condition = condition
        self._strategy = strategy

    async def wait(self) -> None:
        """Wait for condition to be met."""

        await self._strategy.wait(self._condition)
