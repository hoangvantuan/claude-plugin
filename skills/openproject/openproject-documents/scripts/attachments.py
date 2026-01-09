"""OpenProject Attachments API operations."""

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


def get_attachment(attachment_id: int) -> dict:
    """Get attachment metadata."""
    with get_client() as client:
        return client.get(f"/attachments/{attachment_id}")


def list_attachments(
    container_type: str,
    container_id: int,
    page_size: int = 100
) -> Iterator[dict]:
    """List attachments for a container.

    Args:
        container_type: "work_packages", "documents", "wiki_pages"
        container_id: Container ID

    Yields:
        Attachment dicts
    """
    with get_client() as client:
        yield from paginate(
            client,
            f"/{container_type}/{container_id}/attachments",
            page_size=page_size
        )


def download_attachment(attachment_id: int, output_path: str) -> str:
    """Download attachment to local path.

    Args:
        attachment_id: Attachment ID
        output_path: Local path to save file

    Returns:
        Output path
    """
    with get_client() as client:
        attachment = client.get(f"/attachments/{attachment_id}")
        download_url = attachment["_links"]["downloadLocation"]["href"]

        # Download file (need direct HTTP request)
        response = client.client.get(download_url)
        with open(output_path, "wb") as f:
            f.write(response.content)

        return output_path


def upload_attachment(
    container_type: str,
    container_id: int,
    file_path: str,
    description: Optional[str] = None
) -> dict:
    """Upload file as attachment.

    Args:
        container_type: "work_packages", "documents", "wiki_pages"
        container_id: Container ID
        file_path: Local file path
        description: Optional description

    Returns:
        Created attachment dict
    """
    file_path = Path(file_path)

    with get_client() as client:
        # Step 1: Prepare upload
        prepare_data = {
            "fileName": file_path.name,
            "fileSize": file_path.stat().st_size
        }

        if description:
            prepare_data["description"] = {"raw": description}

        prepared = client.post(
            f"/{container_type}/{container_id}/attachments/prepare",
            prepare_data
        )

        # Step 2: Upload to provided URL
        upload_url = prepared["_links"]["uploadLink"]["href"]
        with open(file_path, "rb") as f:
            client.client.put(upload_url, content=f.read())

        return prepared


def delete_attachment(attachment_id: int) -> dict:
    """Delete an attachment."""
    with get_client() as client:
        return client.delete(f"/attachments/{attachment_id}")
