"""OpenProject Roles API operations."""

from typing import Iterator

from openproject_core import OpenProjectClient, paginate


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_roles(page_size: int = 100) -> Iterator[dict]:
    """List all roles."""
    with get_client() as client:
        yield from paginate(client, "/roles", page_size=page_size)


def get_role(role_id: int) -> dict:
    """Get role with permissions list."""
    with get_client() as client:
        return client.get(f"/roles/{role_id}")
