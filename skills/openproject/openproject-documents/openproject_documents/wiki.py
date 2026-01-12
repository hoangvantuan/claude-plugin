"""OpenProject Wiki API operations."""

from typing import Iterator, Optional

from openproject_core import OpenProjectClient, paginate


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def get_wiki_page(page_id: int) -> dict:
    """Get wiki page content."""
    with get_client() as client:
        return client.get(f"/wiki_pages/{page_id}")


def list_wiki_attachments(
    page_id: int,
    page_size: int = 100
) -> Iterator[dict]:
    """Get wiki page attachments.

    Args:
        page_id: Wiki page ID

    Yields:
        Attachment dicts
    """
    with get_client() as client:
        yield from paginate(
            client,
            f"/wiki_pages/{page_id}/attachments",
            page_size=page_size
        )


def update_wiki_page(
    page_id: int,
    title: Optional[str] = None,
    text: Optional[str] = None
) -> dict:
    """Update wiki page.

    Args:
        page_id: Wiki page ID
        title: New title
        text: New content (raw markdown)

    Returns:
        Updated wiki page dict
    """
    data = {}

    if title:
        data["title"] = title

    if text:
        data["text"] = {"raw": text}

    with get_client() as client:
        return client.patch(f"/wiki_pages/{page_id}", data)
