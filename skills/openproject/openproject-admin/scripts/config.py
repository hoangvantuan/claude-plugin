"""OpenProject Configuration API operations."""

import sys
from pathlib import Path

# Add openproject-core scripts to path
_core_scripts = Path(__file__).parent.parent.parent / "openproject-core" / "scripts"
sys.path.insert(0, str(_core_scripts))

from client import OpenProjectClient


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
