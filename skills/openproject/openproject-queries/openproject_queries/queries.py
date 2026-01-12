"""OpenProject Queries API operations."""

from typing import Iterator, List, Optional, Tuple

from openproject_core import OpenProjectClient, build_filters, build_sort, paginate


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_queries(
    project_id: Optional[int] = None,
    page_size: int = 100
) -> Iterator[dict]:
    """List queries, optionally filtered by project.

    Args:
        project_id: Filter by project ID

    Yields:
        Query dicts
    """
    with get_client() as client:
        params = {}
        if project_id:
            filters = [{"project_id": {"operator": "=", "values": [str(project_id)]}}]
            params["filters"] = build_filters(filters)

        yield from paginate(client, "/queries", params, page_size)


def get_query(query_id: int) -> dict:
    """Get query with full filter/column configuration."""
    with get_client() as client:
        return client.get(f"/queries/{query_id}")


def create_query(
    name: str,
    project_id: Optional[int] = None,
    filters: Optional[List[dict]] = None,
    columns: Optional[List[str]] = None,
    sort_by: Optional[List[Tuple[str, str]]] = None,
    group_by: Optional[str] = None,
    public: bool = False
) -> dict:
    """Create saved query.

    Args:
        name: Query name
        project_id: Project scope (None for global)
        filters: Filter configuration
        columns: Columns to display
        sort_by: Sort configuration [(field, direction), ...]
        group_by: Group by field
        public: Make query visible to others

    Returns:
        Created query dict
    """
    data = {
        "name": name,
        "public": public
    }

    if filters:
        data["filters"] = filters

    if columns:
        data["columns"] = columns

    if sort_by:
        data["sortBy"] = [[field, direction] for field, direction in sort_by]

    if group_by:
        data["groupBy"] = group_by

    # Add project link if specified
    if project_id:
        data["_links"] = {
            "project": {"href": f"/projects/{project_id}"}
        }

    with get_client() as client:
        return client.post("/queries", data)


def update_query(query_id: int, **updates) -> dict:
    """Update query configuration.

    Updatable: name, filters, columns, sortBy, groupBy, public
    """
    data = {}

    if "name" in updates:
        data["name"] = updates["name"]

    if "public" in updates:
        data["public"] = updates["public"]

    if "filters" in updates:
        data["filters"] = updates["filters"]

    if "columns" in updates:
        data["columns"] = updates["columns"]

    if "sort_by" in updates:
        data["sortBy"] = [[f, d] for f, d in updates["sort_by"]]

    if "group_by" in updates:
        data["groupBy"] = updates["group_by"]

    with get_client() as client:
        return client.patch(f"/queries/{query_id}", data)


def delete_query(query_id: int) -> dict:
    """Delete query."""
    with get_client() as client:
        return client.delete(f"/queries/{query_id}")


def star_query(query_id: int) -> dict:
    """Add query to favorites."""
    with get_client() as client:
        return client.patch(f"/queries/{query_id}/star", {})


def unstar_query(query_id: int) -> dict:
    """Remove query from favorites."""
    with get_client() as client:
        return client.patch(f"/queries/{query_id}/unstar", {})


def get_query_default() -> dict:
    """Get default query configuration."""
    with get_client() as client:
        return client.get("/queries/default")


def get_available_columns() -> List[dict]:
    """Get available columns for queries."""
    with get_client() as client:
        schema = client.get("/queries/schema")
        return schema.get("columns", {}).get("_links", {}).get("allowedValues", [])
