import asyncio
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable


class WaitCondition(ABC):
    """Base class for all wait conditions."""

    @abstractmethod
    async def check(self) -> None:
        """Check if condition is met. If not, raise an exception."""

        pass


class CallableCondition(WaitCondition):
    """Wait condition that uses a callable."""

    def __init__(self, c: Callable[[], Awaitable[None]]) -> None:
        self._callable = c

    async def check(self) -> None:
        await self._callable()


class CommandCondition(WaitCondition):
    """Wait condition that uses a command."""

    class CommandError(Exception):
        """Raised when a command fails."""

        def __init__(self, code: int, stdout: bytes, stderr: bytes) -> None:
            stdout = stdout.decode()
            stderr = stderr.decode()

            message = f"Command failed with code {code}."
            if stdout:
                message = f"{message}\n{stdout}"
            if stderr:
                message = f"{message}\n{stderr}"

            super().__init__(message)

    def __init__(self, command: list[str], env: dict[str, str] = None) -> None:
        self._command = command
        self._env = env

    async def check(self) -> None:
        process = await asyncio.create_subprocess_exec(
            *self._command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=self._env,
        )

        stdout, stderr = await process.communicate()
        code = process.returncode

        if code == 0:
            return

        raise self.CommandError(code, stdout, stderr)
