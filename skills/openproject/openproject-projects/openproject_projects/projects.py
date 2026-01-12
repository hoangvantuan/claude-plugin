"""OpenProject Projects API operations."""

from typing import Optional, Iterator, Union

from openproject_core import OpenProjectClient, build_filters, build_sort, paginate


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_projects(
    filters: Optional[list[dict]] = None,
    sort_by: Optional[list[tuple[str, str]]] = None,
    page_size: int = 100
) -> Iterator[dict]:
    """List all projects with optional filters.

    Args:
        filters: Filter conditions
            - active: "t" or "f"
            - ancestor: project ID
            - name_and_identifier: search string
            - parent_id: parent project ID

        sort_by: Sort criteria, e.g. [("name", "asc")]

    Yields:
        Project dicts
    """
    with get_client() as client:
        params = {}
        if filters:
            params["filters"] = build_filters(filters)
        if sort_by:
            params["sortBy"] = build_sort(sort_by)

        yield from paginate(client, "/projects", params, page_size)


def get_project(project_id: Union[int, str]) -> dict:
    """Get single project by ID or identifier.

    Args:
        project_id: Numeric ID or string identifier

    Returns:
        Project dict with _links, _embedded
    """
    with get_client() as client:
        return client.get(f"/projects/{project_id}")


def create_project(
    name: str,
    identifier: Optional[str] = None,
    description: Optional[str] = None,
    public: bool = False,
    parent_id: Optional[int] = None,
    **custom_fields
) -> dict:
    """Create new project.

    Args:
        name: Project name (required)
        identifier: URL-friendly identifier (auto-generated if not provided)
        description: Project description
        public: Whether project is public
        parent_id: Parent project ID for hierarchy
        **custom_fields: Additional custom field values

    Returns:
        Created project dict
    """
    data = {
        "name": name,
        "public": public
    }

    if identifier:
        data["identifier"] = identifier
    if description:
        data["description"] = {"raw": description}
    if parent_id:
        data["_links"] = {
            "parent": {"href": f"/projects/{parent_id}"}
        }

    # Add custom fields
    data.update(custom_fields)

    with get_client() as client:
        return client.post("/projects", data)


def update_project(project_id: Union[int, str], **updates) -> dict:
    """Update existing project.

    Args:
        project_id: Project ID or identifier
        **updates: Fields to update (name, description, public, etc.)

    Returns:
        Updated project dict
    """
    data = {}

    if "name" in updates:
        data["name"] = updates["name"]
    if "description" in updates:
        data["description"] = {"raw": updates["description"]}
    if "public" in updates:
        data["public"] = updates["public"]
    if "active" in updates:
        data["active"] = updates["active"]

    # Handle parent link
    if "parent_id" in updates:
        parent_id = updates["parent_id"]
        data.setdefault("_links", {})
        if parent_id:
            data["_links"]["parent"] = {"href": f"/projects/{parent_id}"}
        else:
            data["_links"]["parent"] = {"href": None}

    with get_client() as client:
        return client.patch(f"/projects/{project_id}", data)


def delete_project(project_id: Union[int, str]) -> dict:
    """Delete project.

    Args:
        project_id: Project ID or identifier

    Returns:
        Empty dict on success
    """
    with get_client() as client:
        return client.delete(f"/projects/{project_id}")


def copy_project(
    project_id: Union[int, str],
    new_name: str,
    new_identifier: Optional[str] = None
) -> dict:
    """Copy project with new name.

    Args:
        project_id: Source project ID
        new_name: Name for copied project
        new_identifier: Identifier for copied project

    Returns:
        Copied project dict
    """
    data = {"name": new_name}
    if new_identifier:
        data["identifier"] = new_identifier

    with get_client() as client:
        return client.post(f"/projects/{project_id}/copy", data)


def get_versions(project_id: Union[int, str]) -> Iterator[dict]:
    """List versions in project.

    Yields:
        Version dicts
    """
    with get_client() as client:
        yield from paginate(client, f"/projects/{project_id}/versions")


def get_categories(project_id: Union[int, str]) -> Iterator[dict]:
    """List categories in project.

    Yields:
        Category dicts
    """
    with get_client() as client:
        yield from paginate(client, f"/projects/{project_id}/categories")


def get_types(project_id: Union[int, str]) -> Iterator[dict]:
    """List work package types enabled in project.

    Yields:
        Type dicts
    """
    with get_client() as client:
        yield from paginate(client, f"/projects/{project_id}/types")


def toggle_favorite(project_id: Union[int, str], favorite: bool = True) -> dict:
    """Add or remove project from favorites.

    Args:
        project_id: Project ID
        favorite: True to add, False to remove

    Returns:
        Response dict
    """
    with get_client() as client:
        if favorite:
            return client.post(f"/projects/{project_id}/favorite")
        else:
            return client.delete(f"/projects/{project_id}/favorite")
