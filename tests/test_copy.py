from pathlib import Path

import copier
import pytest


@pytest.fixture
def data() -> dict[str, str]:
    """Return a dictionary with the data to be used in the template."""
    return {
        "accountname": "foo",
        "servicename": "foo",
        "description": "Example service",
    }


def test_copy(
    tmp_path_factory: pytest.TempPathFactory,
    cloned_template_directory: Path,
    data: dict[str, str],
) -> None:
    """Test that the template can be copied without errors using defaults."""
    tmp_path = tmp_path_factory.mktemp("copied-template-")

    copier.run_copy(
        str(cloned_template_directory),
        str(tmp_path),
        defaults=True,
        data=data,
        vcs_ref="HEAD",
        quiet=True,
    )
