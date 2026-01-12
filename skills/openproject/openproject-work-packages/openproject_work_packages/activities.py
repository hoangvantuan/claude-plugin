"""Work package activities (comments, history)."""

from typing import Iterator

from openproject_core import OpenProjectClient, paginate


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
