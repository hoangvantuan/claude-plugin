"""Custom exceptions for OpenProject API."""


class OpenProjectError(Exception):
    """Base exception for OpenProject errors."""
    pass


class AuthenticationError(OpenProjectError):
    """Authentication failed."""
    pass


class OpenProjectAPIError(OpenProjectError):
    """API returned an error response."""

    def __init__(self, status_code: int, message: str, error_id: str = None):
        self.status_code = status_code
        self.message = message
        self.error_id = error_id
        super().__init__(f"[{status_code}] {message}")
