"""OpenProject Work Packages API operations."""

from typing import Optional, Iterator, Union

from openproject_core import OpenProjectClient, build_filters, build_sort, paginate

API_V3_PREFIX = "/api/v3"


def _to_href(resource: str, value: Union[int, str]) -> str:
    """Build /api/v3 href from ID or full path."""
    s = str(value)
    if s.startswith(f"{API_V3_PREFIX}/"):
        return s
    return f"{API_V3_PREFIX}/{resource}/{value}"


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
    type_id: Optional[Union[int, str]] = None,
    description: Optional[Union[str, dict]] = None,
    assignee_id: Optional[Union[int, str]] = None,
    status_id: Optional[Union[int, str]] = None,
    priority_id: Optional[Union[int, str]] = None,
    parent_id: Optional[Union[int, str]] = None,
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

    # Build _links with /api/v3 prefix
    links["project"] = {"href": _to_href("projects", project_id)}

    if type_id:
        links["type"] = {"href": _to_href("types", type_id)}
    if assignee_id:
        links["assignee"] = {"href": _to_href("users", assignee_id)}
    if status_id:
        links["status"] = {"href": _to_href("statuses", status_id)}
    if priority_id:
        links["priority"] = {"href": _to_href("priorities", priority_id)}
    if parent_id:
        links["parent"] = {"href": _to_href("work_packages", parent_id)}

    data["_links"] = links

    # Add scalar fields
    if description:
        if isinstance(description, dict):
            data["description"] = description
        else:
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

    Automatically fetches lockVersion if not provided to prevent 409 Conflict.

    Args:
        wp_id: Work package ID
        **updates: Fields to update:
            - lockVersion: Optional, auto-fetched if omitted
            - subject, description, start_date, due_date, done_ratio
            - status_id, assignee_id, type_id, priority_id, parent_id, version_id
            - customFieldN: Custom fields (e.g., customField8=3)

    Returns:
        Updated work package dict
    """
    # Auto-fetch lockVersion if not provided
    if "lockVersion" not in updates:
        current = get_work_package(wp_id)
        updates["lockVersion"] = current.get("lockVersion")

    data = {}
    links = {}

    # Track processed fields to forward remaining kwargs
    processed = set()

    # 1. Handle lockVersion
    data["lockVersion"] = updates["lockVersion"]
    processed.add("lockVersion")

    # 2. Handle simple scalar fields
    field_mapping = {
        "subject": "subject",
        "start_date": "startDate",
        "due_date": "dueDate",
        "done_ratio": "percentageDone"
    }

    for arg_name, api_name in field_mapping.items():
        if arg_name in updates:
            data[api_name] = updates[arg_name]
            processed.add(arg_name)

    # 3. Handle description (special format)
    if "description" in updates:
        desc = updates["description"]
        if isinstance(desc, dict):
            data["description"] = desc
        else:
            data["description"] = {"raw": desc}
        processed.add("description")

    # 4. Handle estimated_hours (ISO duration format)
    if "estimated_hours" in updates:
        data["estimatedTime"] = f"PT{updates['estimated_hours']}H"
        processed.add("estimated_hours")

    # 5. Handle link fields
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
                links[link_name] = {"href": _to_href(resource, value)}
            else:
                links[link_name] = {"href": None}
            processed.add(arg_name)

    if links:
        data["_links"] = links

    # 6. Forward remaining kwargs (custom fields, etc.)
    for key, value in updates.items():
        if key not in processed:
            data[key] = value

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
