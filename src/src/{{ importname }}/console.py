from rich.console import Console


class FallbackConsoleBuilder:
    """Builds the fallback console."""

    def build(self) -> Console:
        return Console()
