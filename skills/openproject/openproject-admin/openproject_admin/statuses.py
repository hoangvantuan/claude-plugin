"""OpenProject Statuses API operations."""

from typing import Iterator

from openproject_core import OpenProjectClient, paginate


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
