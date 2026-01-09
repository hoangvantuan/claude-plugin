"""OpenProject Priorities API operations."""

import sys
from pathlib import Path
from typing import Iterator

# Add openproject-core scripts to path
_core_scripts = Path(__file__).parent.parent.parent / "openproject-core" / "scripts"
sys.path.insert(0, str(_core_scripts))

from client import OpenProjectClient
from helpers import paginate


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_priorities(page_size: int = 100) -> Iterator[dict]:
    """List all priorities."""
    with get_client() as client:
        yield from paginate(client, "/priorities", page_size=page_size)


def get_priority(priority_id: int) -> dict:
    """Get priority details."""
    with get_client() as client:
        return client.get(f"/priorities/{priority_id}")


def get_default_priority() -> dict:
    """Get the default priority."""
    for priority in list_priorities():
        if priority.get("isDefault", False):
            return priority
    return {}
