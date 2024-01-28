from pathlib import Path

import pytest
from plumbum import local

from tests.utils import CWD, IgnoreGitConfig, SandboxedGitRepo


@pytest.fixture()
def root_directory() -> Path:
    """Return the root directory of the project."""

    return Path(__file__).parent.parent.resolve()


@pytest.fixture()
def tracked_files(root_directory: Path) -> list[Path]:
    """Return a list of all tracked files (including unstaged) in the project."""

    with CWD(root_directory):
        with IgnoreGitConfig():
            common_options = ["--full-name", "--exclude-standard"]
            cached = local.cmd.git("ls-files", "--cached", *common_options)
            others = local.cmd.git("ls-files", "--others", *common_options)

    all = sorted(set(cached.splitlines() + others.splitlines()))
    return [Path(path) for path in all]


@pytest.fixture()
def cloned_template_directory(
    tmp_path_factory: pytest.TempPathFactory,
    root_directory: Path,
    tracked_files: list[Path],
) -> Path:
    """Return a temporary directory with a cloned copy of the repository."""

    tmp_path = tmp_path_factory.mktemp("cloned-template-repo-")

    with CWD(root_directory):
        local.cmd.cp("--parents", *tracked_files, tmp_path)

    with SandboxedGitRepo(tmp_path):
        local.cmd.git("add", "./")
        local.cmd.git("commit", "--message", "Initial commit")
        yield tmp_path
