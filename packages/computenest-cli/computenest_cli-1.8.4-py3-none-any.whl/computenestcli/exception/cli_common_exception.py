class CliCommonException(Exception):
    """A custom exception class for handling application-specific errors."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{self.message}"
