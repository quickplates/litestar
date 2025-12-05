class WaitError(Exception):
    """Raised when a wait operation fails."""


class GivenUpError(WaitError):
    """Raised when a wait strategy gives up."""

    def __init__(self) -> None:
        super().__init__("Wait strategy gave up.")
