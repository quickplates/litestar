import asyncio
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable, Mapping, Sequence
from typing import override


class WaitCondition(ABC):
    """Base class for all wait conditions."""

    @abstractmethod
    async def check(self) -> None:
        """Check if condition is met. If not, raise an exception."""


class CallableCondition(WaitCondition):
    """Wait condition that uses a callable."""

    def __init__(self, c: Callable[[], Awaitable[None]]) -> None:
        self._callable = c

    @override
    async def check(self) -> None:
        await self._callable()


class CommandCondition(WaitCondition):
    """Wait condition that uses a command."""

    class CommandError(Exception):
        """Raised when a command fails."""

        def __init__(self, code: int, stdout: bytes, stderr: bytes) -> None:
            out = stdout.decode()
            err = stderr.decode()

            message = f"Command failed with code {code}."
            if out:
                message = f"{message}\n{out}"
            if err:
                message = f"{message}\n{err}"

            super().__init__(message)

    def __init__(
        self, command: Sequence[str], env: Mapping[str, str] | None = None
    ) -> None:
        self._command = command
        self._env = env

    @override
    async def check(self) -> None:
        process = await asyncio.create_subprocess_exec(
            *self._command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=self._env,
        )

        stdout, stderr = await process.communicate()
        code = process.returncode

        if not code:
            return

        raise self.CommandError(code, stdout, stderr)
