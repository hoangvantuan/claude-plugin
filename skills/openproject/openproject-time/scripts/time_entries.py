"""OpenProject Time Entries API operations."""

import sys
from pathlib import Path
from typing import Optional, Iterator, Union, List, Tuple
from datetime import date

# Add openproject-core scripts to path
_core_scripts = Path(__file__).parent.parent.parent / "openproject-core" / "scripts"
sys.path.insert(0, str(_core_scripts))

from client import OpenProjectClient
from helpers import build_filters, build_sort, paginate


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_time_entries(
    filters: Optional[List[dict]] = None,
    sort_by: Optional[List[Tuple[str, str]]] = None,
    page_size: int = 100
) -> Iterator[dict]:
    """List time entries with filters.

    Common filters:
        - user: User ID or "me"
        - project: Project ID
        - work_package: Work package ID
        - spent_on: Date or date range
        - activity: Activity type ID

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
    """Get all time entries for a work package."""
    return list(list_time_entries(filters=[
        {"work_package": {"operator": "=", "values": [str(wp_id)]}}
    ]))
