"""OpenProject Types API operations."""

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


def list_types(page_size: int = 100) -> Iterator[dict]:
    """List work package types (Task, Bug, Feature, etc.)."""
    with get_client() as client:
        yield from paginate(client, "/types", page_size=page_size)


def get_type(type_id: int) -> dict:
    """Get type details including color, icon."""
    with get_client() as client:
        return client.get(f"/types/{type_id}")


def list_project_types(project_id: int, page_size: int = 100) -> Iterator[dict]:
    """List types available in a specific project."""
    with get_client() as client:
        yield from paginate(
            client,
            f"/projects/{project_id}/types",
            page_size=page_size
        )
