from pathlib import Path
from types import TracebackType

from plumbum import local


class CWD:
    """Context manager to change the current working directory."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._cwd = None

    def __enter__(self) -> Path:
        self._cwd = local.cwd(self._path)
        self._cwd.__enter__()
        return self._path

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        if self._cwd is None:
            return False
        return self._cwd.__exit__(exception_type, exception, traceback)


class IgnoreGitConfig:
    """Context manager to ignore global git config files."""

    def __init__(self) -> None:
        self._env = None

    def __enter__(self) -> None:
        self._env = local.env(GIT_CONFIG_GLOBAL="", GIT_CONFIG_SYSTEM="")
        self._env.__enter__()

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        if self._env is None:
            return False
        return self._env.__exit__(exception_type, exception, traceback)


class SandboxedGitRepo:
    """Context manager to create a sandboxed git repository."""

    def __init__(
        self, path: Path, username: str = "test", email: str = "test@example.org"
    ) -> None:
        self._cwd = CWD(path)
        self._ignore_git_config = IgnoreGitConfig()
        self._username = username
        self._email = email

    def __enter__(self) -> None:
        self._cwd.__enter__()
        self._ignore_git_config.__enter__()
        local.cmd.git("init")
        local.cmd.git("config", "--local", "user.name", self._username)
        local.cmd.git("config", "--local", "user.email", self._email)

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        cwd_return = self._cwd.__exit__(exception_type, exception, traceback)
        ignore_git_config_return = self._ignore_git_config.__exit__(
            exception_type, exception, traceback
        )
        return cwd_return or ignore_git_config_return
