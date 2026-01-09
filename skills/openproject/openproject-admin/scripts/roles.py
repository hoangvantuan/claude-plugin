"""OpenProject Roles API operations."""

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


def list_roles(page_size: int = 100) -> Iterator[dict]:
    """List all roles."""
    with get_client() as client:
        yield from paginate(client, "/roles", page_size=page_size)


def get_role(role_id: int) -> dict:
    """Get role with permissions list."""
    with get_client() as client:
        return client.get(f"/roles/{role_id}")
