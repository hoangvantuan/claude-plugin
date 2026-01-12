"""OpenProject Memberships API operations."""

from typing import Iterator, List, Optional

from openproject_core import OpenProjectClient, build_filters, paginate


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_memberships(
    project_id: Optional[int] = None,
    principal_id: Optional[int] = None,
    page_size: int = 100
) -> Iterator[dict]:
    """List memberships.

    Args:
        project_id: Filter by project
        principal_id: Filter by user/group
    """
    with get_client() as client:
        filters = []
        if project_id:
            filters.append({"project": {"operator": "=", "values": [str(project_id)]}})
        if principal_id:
            filters.append({"principal": {"operator": "=", "values": [str(principal_id)]}})

        params = {}
        if filters:
            params["filters"] = build_filters(filters)

        yield from paginate(client, "/memberships", params, page_size)


def get_membership(membership_id: int) -> dict:
    """Get membership details."""
    with get_client() as client:
        return client.get(f"/memberships/{membership_id}")


def create_membership(
    project_id: int,
    principal_id: int,
    role_ids: List[int],
    notification_message: Optional[str] = None
) -> dict:
    """Add user/group to project with roles.

    Args:
        project_id: Target project
        principal_id: User or group ID
        role_ids: List of role IDs to assign
        notification_message: Custom notification message
    """
    data = {
        "_links": {
            "project": {"href": f"/projects/{project_id}"},
            "principal": {"href": f"/principals/{principal_id}"},
            "roles": [{"href": f"/roles/{rid}"} for rid in role_ids]
        }
    }

    if notification_message:
        data["_meta"] = {"notificationMessage": {"raw": notification_message}}

    with get_client() as client:
        return client.post("/memberships", data)


def update_membership(membership_id: int, role_ids: List[int]) -> dict:
    """Update membership roles."""
    data = {
        "_links": {
            "roles": [{"href": f"/roles/{rid}"} for rid in role_ids]
        }
    }

    with get_client() as client:
        return client.patch(f"/memberships/{membership_id}", data)


def delete_membership(membership_id: int) -> dict:
    """Remove membership (remove user/group from project)."""
    with get_client() as client:
        return client.delete(f"/memberships/{membership_id}")
