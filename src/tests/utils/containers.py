import asyncio

from testcontainers.core.container import DockerContainer


class AsyncDockerContainer(DockerContainer):
    """DockerContainer with async methods."""

    async def __aenter__(self):
        return await asyncio.to_thread(self.__enter__)

    async def __aexit__(self, *args, **kwargs):
        return await asyncio.to_thread(self.__exit__, *args, **kwargs)

    async def aexec(self, *args, **kwargs):
        return await asyncio.to_thread(self.exec, *args, **kwargs)
