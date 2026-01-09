"""OpenProject Documents API operations."""

import sys
from pathlib import Path
from typing import Optional, Iterator

# Add openproject-core scripts to path
_core_scripts = Path(__file__).parent.parent.parent / "openproject-core" / "scripts"
sys.path.insert(0, str(_core_scripts))

from client import OpenProjectClient
from helpers import paginate


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_documents(
    project_id: int,
    page_size: int = 100
) -> Iterator[dict]:
    """List documents in a project.

    Args:
        project_id: Project ID

    Yields:
        Document dicts
    """
    with get_client() as client:
        yield from paginate(client, f"/projects/{project_id}/documents", page_size=page_size)


def get_document(document_id: int) -> dict:
    """Get document details."""
    with get_client() as client:
        return client.get(f"/documents/{document_id}")


def create_document(
    project_id: int,
    title: str,
    description: Optional[str] = None
) -> dict:
    """Create a document in a project.

    Args:
        project_id: Project ID
        title: Document title
        description: Document description

    Returns:
        Created document dict
    """
    data = {
        "title": title,
        "_links": {
            "project": {"href": f"/projects/{project_id}"}
        }
    }

    if description:
        data["description"] = {"raw": description}

    with get_client() as client:
        return client.post("/documents", data)


def delete_document(document_id: int) -> dict:
    """Delete a document."""
    with get_client() as client:
        return client.delete(f"/documents/{document_id}")
