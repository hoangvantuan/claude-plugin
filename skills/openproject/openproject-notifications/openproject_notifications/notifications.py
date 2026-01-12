"""OpenProject Notifications API operations."""

from typing import Iterator, Optional

from openproject_core import OpenProjectClient, build_filters, paginate


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_notifications(
    read_status: Optional[bool] = None,
    reason: Optional[str] = None,
    page_size: int = 100
) -> Iterator[dict]:
    """List notifications.

    Args:
        read_status: True for read, False for unread, None for all
        reason: Filter by reason (mentioned, assigned, watched, etc.)

    Yields:
        Notification dicts
    """
    with get_client() as client:
        filters = []

        if read_status is not None:
            filters.append({
                "readIAN": {"operator": "=", "values": ["t" if read_status else "f"]}
            })

        if reason:
            filters.append({
                "reason": {"operator": "=", "values": [reason]}
            })

        params = {}
        if filters:
            params["filters"] = build_filters(filters)

        yield from paginate(client, "/notifications", params, page_size)


def get_notification(notification_id: int) -> dict:
    """Get notification details."""
    with get_client() as client:
        return client.get(f"/notifications/{notification_id}")


def mark_read(notification_id: int) -> dict:
    """Mark notification as read."""
    with get_client() as client:
        return client.post(f"/notifications/{notification_id}/read_ian", {})


def mark_unread(notification_id: int) -> dict:
    """Mark notification as unread."""
    with get_client() as client:
        return client.post(f"/notifications/{notification_id}/unread_ian", {})


def mark_all_read() -> dict:
    """Mark all notifications as read."""
    with get_client() as client:
        return client.post("/notifications/read_ian", {})


def get_unread_count() -> int:
    """Get count of unread notifications."""
    with get_client() as client:
        # Use pagination with pageSize=1 to get total count
        response = client.get("/notifications", params={
            "filters": build_filters([{"readIAN": {"operator": "=", "values": ["f"]}}]),
            "pageSize": 1
        })
        return response.get("total", 0)


def list_unread() -> Iterator[dict]:
    """List unread notifications only."""
    return list_notifications(read_status=False)


def list_by_reason(reason: str) -> Iterator[dict]:
    """List notifications by reason.

    Common reasons:
        - mentioned: Mentioned in a comment
        - assigned: Assigned to a work package
        - watched: Watching a work package
        - responsible: Accountable for a work package
        - commented: Someone commented
        - created: Work package created
        - prioritized: Priority changed
        - scheduled: Date changed
    """
    return list_notifications(reason=reason)
