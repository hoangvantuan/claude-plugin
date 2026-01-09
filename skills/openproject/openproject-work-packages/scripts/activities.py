"""Work package activities (comments, history)."""

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


def list_activities(wp_id: int) -> Iterator[dict]:
    """List all activities (comments, changes) on work package.

    Yields:
        Activity dicts with _type (Activity::Comment, Activity::Journal)
    """
    with get_client() as client:
        yield from paginate(client, f"/work_packages/{wp_id}/activities")


def add_comment(wp_id: int, comment: str) -> dict:
    """Add comment to work package.

    Args:
        wp_id: Work package ID
        comment: Comment text (supports markdown)

    Returns:
        Created activity dict
    """
    data = {
        "comment": {"raw": comment}
    }

    with get_client() as client:
        return client.post(f"/work_packages/{wp_id}/activities", data)


def get_activity(activity_id: int) -> dict:
    """Get single activity by ID."""
    with get_client() as client:
        return client.get(f"/activities/{activity_id}")
