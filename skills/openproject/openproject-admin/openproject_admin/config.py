"""OpenProject Configuration API operations."""

from openproject_core import OpenProjectClient


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def get_configuration() -> dict:
    """Get system configuration.

    Returns instance settings like:
    - perPageOptions
    - dateFormat
    - timeFormat
    - startOfWeek
    - etc.
    """
    with get_client() as client:
        return client.get("/configuration")
