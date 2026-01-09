"""OpenProject Statuses API operations."""

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


def list_statuses(page_size: int = 100) -> Iterator[dict]:
    """List all statuses (New, In Progress, Closed, etc.)."""
    with get_client() as client:
        yield from paginate(client, "/statuses", page_size=page_size)


def get_status(status_id: int) -> dict:
    """Get status details including color, isClosed flag."""
    with get_client() as client:
        return client.get(f"/statuses/{status_id}")


def list_open_statuses() -> Iterator[dict]:
    """List only open statuses."""
    for status in list_statuses():
        if not status.get("isClosed", False):
            yield status


def list_closed_statuses() -> Iterator[dict]:
    """List only closed statuses."""
    for status in list_statuses():
        if status.get("isClosed", False):
            yield status
