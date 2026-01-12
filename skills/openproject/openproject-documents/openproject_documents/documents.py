"""OpenProject Documents API operations.

NOTE: The Documents API is read-only. Creating and deleting documents
is only possible through the OpenProject web UI.
"""

from typing import Iterator

from openproject_core import OpenProjectClient, paginate


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_documents(page_size: int = 100) -> Iterator[dict]:
    """List all documents the user can access.

    NOTE: API does not support filtering by project.
    Filter client-side if needed.

    Yields:
        Document dicts with id, title, description, project link
    """
    with get_client() as client:
        yield from paginate(client, "/documents", page_size=page_size)


def get_document(document_id: int) -> dict:
    """Get document details.

    Args:
        document_id: Document ID

    Returns:
        Document dict with title, description, attachments, project
    """
    with get_client() as client:
        return client.get(f"/documents/{document_id}")


# NOTE: create_document and delete_document removed
# API v3 does not support creating or deleting documents
# Use the OpenProject web UI instead
