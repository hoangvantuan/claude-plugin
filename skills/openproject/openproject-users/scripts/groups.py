"""OpenProject Groups API operations."""

import sys
from pathlib import Path
from typing import Optional, Iterator, List

# Add openproject-core scripts to path
_core_scripts = Path(__file__).parent.parent.parent / "openproject-core" / "scripts"
sys.path.insert(0, str(_core_scripts))

from client import OpenProjectClient
from helpers import paginate


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_groups(page_size: int = 100) -> Iterator[dict]:
    """List all groups."""
    with get_client() as client:
        yield from paginate(client, "/groups", page_size=page_size)


def get_group(group_id: int) -> dict:
    """Get group with members."""
    with get_client() as client:
        return client.get(f"/groups/{group_id}")


def create_group(name: str, member_ids: Optional[List[int]] = None) -> dict:
    """Create group.

    Args:
        name: Group name
        member_ids: Initial member user IDs
    """
    data = {"name": name}

    if member_ids:
        data["_links"] = {
            "members": [{"href": f"/users/{uid}"} for uid in member_ids]
        }

    with get_client() as client:
        return client.post("/groups", data)


def update_group(
    group_id: int,
    name: Optional[str] = None,
    member_ids: Optional[List[int]] = None
) -> dict:
    """Update group name or members."""
    data = {}

    if name:
        data["name"] = name
    if member_ids is not None:
        data["_links"] = {
            "members": [{"href": f"/users/{uid}"} for uid in member_ids]
        }

    with get_client() as client:
        return client.patch(f"/groups/{group_id}", data)


def delete_group(group_id: int) -> dict:
    """Delete group."""
    with get_client() as client:
        return client.delete(f"/groups/{group_id}")


def add_member(group_id: int, user_id: int) -> dict:
    """Add user to group."""
    group = get_group(group_id)
    members_links = group.get("_links", {}).get("members", [])
    current_ids = [int(m["href"].split("/")[-1]) for m in members_links]

    if user_id not in current_ids:
        current_ids.append(user_id)

    return update_group(group_id, member_ids=current_ids)


def remove_member(group_id: int, user_id: int) -> dict:
    """Remove user from group."""
    group = get_group(group_id)
    members_links = group.get("_links", {}).get("members", [])
    current_ids = [int(m["href"].split("/")[-1]) for m in members_links]

    if user_id in current_ids:
        current_ids.remove(user_id)

    return update_group(group_id, member_ids=current_ids)
