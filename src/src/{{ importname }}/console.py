from rich.console import Console


class FallbackConsoleBuilder:
    """Builds the fallback console."""

    def build(self) -> Console:
        """Build the console."""
        return Console()
