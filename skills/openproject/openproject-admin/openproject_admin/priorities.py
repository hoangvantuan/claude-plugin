"""OpenProject Priorities API operations."""

from typing import Iterator

from openproject_core import OpenProjectClient, paginate


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
