import asyncio
from types import TracebackType
from typing import Self

from testcontainers.core.container import DockerContainer


class AsyncDockerContainer(DockerContainer):
    """DockerContainer with async methods."""

    async def __aenter__(self) -> Self:
        """Enter context."""
        return await asyncio.to_thread(self.__enter__)

    async def __aexit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit context."""
        return await asyncio.to_thread(
            self.__exit__, exception_type, exception, traceback
        )

    async def aexec(self, command: str | list[str]) -> tuple[int, bytes]:
        """Execute."""
        return await asyncio.to_thread(self.exec, command)
