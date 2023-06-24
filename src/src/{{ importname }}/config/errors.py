class ConfigError(Exception):
    """Base class for config errors."""

    pass


class ConfigParseError(ConfigError, ValueError):
    """Raised when config parsing fails."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__("Failed to parse config!", *args, **kwargs)
