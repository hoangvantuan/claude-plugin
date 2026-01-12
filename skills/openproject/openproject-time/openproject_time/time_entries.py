"""OpenProject Time Entries API operations."""

import re
from datetime import date
from typing import Iterator, List, Optional, Tuple, Union

from openproject_core import OpenProjectClient, build_filters, build_sort, paginate, extract_id_from_href


def parse_duration(duration_str: str) -> float:
    """Parse ISO 8601 duration to decimal hours.

    Args:
        duration_str: ISO 8601 duration (e.g., 'PT1H30M45S', 'PT2H', 'PT30M')

    Returns:
        Decimal hours (e.g., 1.5125 for PT1H30M45S)

    Examples:
        >>> parse_duration('PT2H')
        2.0
        >>> parse_duration('PT1H30M')
        1.5
        >>> parse_duration('PT45M')
        0.75
        >>> parse_duration('PT1H30M45S')
        1.5125
    """
    if not duration_str or not isinstance(duration_str, str):
        return 0.0

    if not duration_str.startswith('PT'):
        try:
            return float(duration_str)
        except (ValueError, TypeError):
            return 0.0

    hours = 0.0
    h_match = re.search(r'(\d+(?:\.\d+)?)H', duration_str)
    m_match = re.search(r'(\d+(?:\.\d+)?)M', duration_str)
    s_match = re.search(r'(\d+(?:\.\d+)?)S', duration_str)

    if h_match:
        hours += float(h_match.group(1))
    if m_match:
        hours += float(m_match.group(1)) / 60
    if s_match:
        hours += float(s_match.group(1)) / 3600

    return hours


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_time_entries(
    filters: Optional[List[dict]] = None,
    sort_by: Optional[List[Tuple[str, str]]] = None,
    page_size: int = 100
) -> Iterator[dict]:
    """List time entries with filters.

    Valid filters:
        - entity_type: "WorkPackage" or "Meeting"
        - entity_id: Entity IDs (work package or meeting)
        - project_id: Project ID
        - user_id: User ID
        - spent_on: Date or date range
        - activity_id: Activity type ID
        - ongoing: Filter ongoing timers
        - created_at: Creation date
        - updated_at: Update date

    NOTE: Use entity_type + entity_id to filter by work package!
    Example: [{"entity_type": {"operator": "=", "values": ["WorkPackage"]}},
              {"entity_id": {"operator": "=", "values": ["123"]}}]

    Yields:
        Time entry dicts
    """
    with get_client() as client:
        params = {}
        if filters:
            params["filters"] = build_filters(filters)
        if sort_by:
            params["sortBy"] = build_sort(sort_by)

        yield from paginate(client, "/time_entries", params, page_size)


def get_time_entry(entry_id: int) -> dict:
    """Get single time entry."""
    with get_client() as client:
        return client.get(f"/time_entries/{entry_id}")


def create_time_entry(
    work_package_id: int,
    hours: float,
    activity_id: Optional[int] = None,
    comment: Optional[str] = None,
    spent_on: Optional[Union[str, date]] = None,
    user_id: Optional[int] = None
) -> dict:
    """Create time entry.

    Args:
        work_package_id: Work package to log time on
        hours: Hours spent (decimal, e.g., 1.5)
        activity_id: Activity type ID (Development, Design, etc.)
        comment: Description of work done
        spent_on: Date (YYYY-MM-DD), defaults to today
        user_id: User ID (admin only, defaults to current user)

    Returns:
        Created time entry dict
    """
    # Format hours as ISO duration
    hours_str = f"PT{hours}H"

    data = {
        "hours": hours_str,
        "_links": {
            "workPackage": {"href": f"/work_packages/{work_package_id}"}
        }
    }

    if activity_id:
        data["_links"]["activity"] = {"href": f"/time_entries/activities/{activity_id}"}

    if comment:
        data["comment"] = {"raw": comment}

    if spent_on:
        data["spentOn"] = str(spent_on)

    if user_id:
        data["_links"]["user"] = {"href": f"/users/{user_id}"}

    with get_client() as client:
        return client.post("/time_entries", data)


def update_time_entry(entry_id: int, **updates) -> dict:
    """Update time entry.

    Updatable: hours, comment, spent_on, activity_id, work_package_id
    """
    data = {}
    links = {}

    if "hours" in updates:
        data["hours"] = f"PT{updates['hours']}H"

    if "comment" in updates:
        data["comment"] = {"raw": updates["comment"]}

    if "spent_on" in updates:
        data["spentOn"] = str(updates["spent_on"])

    if "activity_id" in updates:
        links["activity"] = {"href": f"/time_entries/activities/{updates['activity_id']}"}

    if "work_package_id" in updates:
        links["workPackage"] = {"href": f"/work_packages/{updates['work_package_id']}"}

    if links:
        data["_links"] = links

    with get_client() as client:
        return client.patch(f"/time_entries/{entry_id}", data)


def delete_time_entry(entry_id: int) -> dict:
    """Delete time entry."""
    with get_client() as client:
        return client.delete(f"/time_entries/{entry_id}")


def list_activities() -> Iterator[dict]:
    """List available time entry activity types.

    Common activities: Development, Design, Testing, Management, etc.
    """
    with get_client() as client:
        # Activities are available via schema
        schema = client.get("/time_entries/schema")
        activity_schema = schema.get("activity", {})
        allowed = activity_schema.get("_links", {}).get("allowedValues", [])

        for activity in allowed:
            yield {
                "href": activity.get("href"),
                "title": activity.get("title")
            }


def get_activity(activity_id: int) -> dict:
    """Get activity type details."""
    with get_client() as client:
        return client.get(f"/time_entries/activities/{activity_id}")


# Utility functions
def log_time(
    work_package_id: int,
    hours: float,
    **kwargs
) -> dict:
    """Alias for create_time_entry."""
    return create_time_entry(work_package_id, hours, **kwargs)


def get_user_time_today(user_id: Union[int, str] = "me") -> List[dict]:
    """Get all time entries for user today."""
    today = date.today().isoformat()
    return list(list_time_entries(filters=[
        {"user": {"operator": "=", "values": [str(user_id)]}},
        {"spent_on": {"operator": "=", "values": [today]}}
    ]))


def get_work_package_time(wp_id: int) -> List[dict]:
    """Get all time entries for a work package.

    Uses entity_type + entity_id filters (NOT work_package filter).

    Args:
        wp_id: Work package ID

    Returns:
        List of time entry dicts for this work package
    """
    filters = [
        {"entity_type": {"operator": "=", "values": ["WorkPackage"]}},
        {"entity_id": {"operator": "=", "values": [str(wp_id)]}}
    ]
    return list(list_time_entries(filters=filters))


def get_work_packages_time(wp_ids: List[int]) -> dict[int, List[dict]]:
    """Get time entries for multiple work packages in one API call.

    Uses entity_type + entity_id filters with multiple values.

    Args:
        wp_ids: List of work package IDs

    Returns:
        Dict mapping wp_id -> list of time entries
    """
    if not wp_ids:
        return {}

    # Use entity_id filter with multiple values
    filters = [
        {"entity_type": {"operator": "=", "values": ["WorkPackage"]}},
        {"entity_id": {"operator": "=", "values": [str(wp_id) for wp_id in wp_ids]}}
    ]
    all_entries = list(list_time_entries(filters=filters))

    # Group by work package
    result: dict[int, List[dict]] = {wp_id: [] for wp_id in wp_ids}

    for entry in all_entries:
        entry_wp_href = entry.get("_links", {}).get("workPackage", {}).get("href", "")
        entry_wp_id = extract_id_from_href(entry_wp_href)
        if entry_wp_id in result:
            result[entry_wp_id].append(entry)

    return result
