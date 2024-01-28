from typer import Typer


class CliBuilder:
    """Builds the CLI app."""

    def build(self) -> Typer:
        return Typer()
