"""OpenProject Work Packages API operations."""

import sys
from pathlib import Path
from typing import Optional, Iterator, Union

# Add openproject-core scripts to path
_core_scripts = Path(__file__).parent.parent.parent / "openproject-core" / "scripts"
sys.path.insert(0, str(_core_scripts))

from client import OpenProjectClient
from helpers import build_filters, build_sort, paginate


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_work_packages(
    filters: Optional[list] = None,
    sort_by: Optional[list] = None,
    project_id: Optional[int] = None,
    page_size: int = 100
) -> Iterator[dict]:
    """List work packages with filters.

    Args:
        filters: Filter conditions (see wp-filters.md)
        sort_by: Sort criteria, e.g. [("updated_at", "desc")]
        project_id: Limit to specific project
        page_size: Items per page

    Yields:
        Work package dicts
    """
    with get_client() as client:
        # Use project-scoped endpoint if project_id provided
        path = f"/projects/{project_id}/work_packages" if project_id else "/work_packages"

        params = {}
        if filters:
            params["filters"] = build_filters(filters)
        if sort_by:
            params["sortBy"] = build_sort(sort_by)

        yield from paginate(client, path, params, page_size)


def get_work_package(wp_id: int) -> dict:
    """Get single work package.

    Returns:
        Work package dict with _links, _embedded
    """
    with get_client() as client:
        return client.get(f"/work_packages/{wp_id}")


def create_work_package(
    project_id: int,
    subject: str,
    type_id: Optional[int] = None,
    description: Optional[str] = None,
    assignee_id: Optional[int] = None,
    status_id: Optional[int] = None,
    priority_id: Optional[int] = None,
    parent_id: Optional[int] = None,
    start_date: Optional[str] = None,
    due_date: Optional[str] = None,
    estimated_hours: Optional[float] = None,
    **custom_fields
) -> dict:
    """Create new work package.

    Args:
        project_id: Target project (required)
        subject: Work package title (required)
        type_id: Type ID (Task, Bug, Feature, etc.)
        description: Rich text description
        assignee_id: Assigned user ID
        status_id: Status ID
        priority_id: Priority ID
        parent_id: Parent work package ID
        start_date: Start date (YYYY-MM-DD)
        due_date: Due date (YYYY-MM-DD)
        estimated_hours: Estimated hours
        **custom_fields: Custom field values

    Returns:
        Created work package dict
    """
    data = {"subject": subject}
    links = {}

    # Build _links
    links["project"] = {"href": f"/projects/{project_id}"}

    if type_id:
        links["type"] = {"href": f"/types/{type_id}"}
    if assignee_id:
        links["assignee"] = {"href": f"/users/{assignee_id}"}
    if status_id:
        links["status"] = {"href": f"/statuses/{status_id}"}
    if priority_id:
        links["priority"] = {"href": f"/priorities/{priority_id}"}
    if parent_id:
        links["parent"] = {"href": f"/work_packages/{parent_id}"}

    data["_links"] = links

    # Add scalar fields
    if description:
        data["description"] = {"raw": description}
    if start_date:
        data["startDate"] = start_date
    if due_date:
        data["dueDate"] = due_date
    if estimated_hours:
        data["estimatedTime"] = f"PT{estimated_hours}H"

    # Add custom fields
    data.update(custom_fields)

    with get_client() as client:
        return client.post(f"/projects/{project_id}/work_packages", data)


def update_work_package(wp_id: int, **updates) -> dict:
    """Update existing work package.

    Args:
        wp_id: Work package ID
        **updates: Fields to update (subject, description, status_id, etc.)

    Returns:
        Updated work package dict
    """
    data = {}
    links = {}

    # Handle simple fields
    field_mapping = {
        "subject": "subject",
        "start_date": "startDate",
        "due_date": "dueDate",
        "done_ratio": "percentageDone"
    }

    for arg_name, api_name in field_mapping.items():
        if arg_name in updates:
            data[api_name] = updates[arg_name]

    if "description" in updates:
        data["description"] = {"raw": updates["description"]}

    if "estimated_hours" in updates:
        data["estimatedTime"] = f"PT{updates['estimated_hours']}H"

    # Handle link fields
    link_mapping = {
        "type_id": ("type", "types"),
        "assignee_id": ("assignee", "users"),
        "status_id": ("status", "statuses"),
        "priority_id": ("priority", "priorities"),
        "parent_id": ("parent", "work_packages"),
        "version_id": ("version", "versions")
    }

    for arg_name, (link_name, resource) in link_mapping.items():
        if arg_name in updates:
            value = updates[arg_name]
            if value:
                links[link_name] = {"href": f"/{resource}/{value}"}
            else:
                links[link_name] = {"href": None}

    if links:
        data["_links"] = links

    with get_client() as client:
        return client.patch(f"/work_packages/{wp_id}", data)


def delete_work_package(wp_id: int) -> dict:
    """Delete work package.

    Returns:
        Empty dict on success
    """
    with get_client() as client:
        return client.delete(f"/work_packages/{wp_id}")


def get_schema(project_id: int, type_id: int) -> dict:
    """Get work package schema for project/type combination.

    Useful for discovering available custom fields and allowed values.
    """
    with get_client() as client:
        return client.get(f"/work_packages/schemas/{project_id}-{type_id}")
