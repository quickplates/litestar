from typer import Typer


class CliBuilder:
    """Builds the CLI app."""

    def build(self) -> Typer:
        """Build the app."""
        return Typer()
