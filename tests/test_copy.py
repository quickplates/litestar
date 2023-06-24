from pathlib import Path

import copier
import pytest


@pytest.fixture()
def data() -> dict[str, str]:
    """Return a dictionary with the data to be used in the template."""

    return {
        "username": "quickplates",
        "email": "quickplates@mail.spietras.dev",
        "projectname": "litestar-example",
        "description": "Litestar project example 🌠",
    }


def test_copy(
    tmp_path_factory: pytest.TempPathFactory,
    cloned_template_directory: Path,
    data: dict[str, str],
) -> None:
    """Test that the template can be copied without errors using defaults."""

    prefix = "copied-template-"

    with tmp_path_factory.mktemp(prefix) as tmp_path:
        copier.run_copy(
            str(cloned_template_directory),
            str(tmp_path),
            defaults=True,
            data=data,
            vcs_ref="HEAD",
            quiet=True,
        )
