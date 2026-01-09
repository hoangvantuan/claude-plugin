"""OpenProject Users API operations."""

import sys
from pathlib import Path
from typing import Optional, Iterator, Union

# Add openproject-core scripts to path
_core_scripts = Path(__file__).parent.parent.parent / "openproject-core" / "scripts"
sys.path.insert(0, str(_core_scripts))

from client import OpenProjectClient
from helpers import build_filters, paginate


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_users(
    filters: Optional[list] = None,
    page_size: int = 100
) -> Iterator[dict]:
    """List users.

    Requires: Admin or manage_user permission

    Filters:
        - status: active, invited, locked
        - group: Group ID
        - name: Name or email search
        - login: User login

    Yields:
        User dicts
    """
    with get_client() as client:
        params = {}
        if filters:
            params["filters"] = build_filters(filters)
        yield from paginate(client, "/users", params, page_size)


def get_user(user_id: Union[int, str]) -> dict:
    """Get user by ID or 'me' for current user."""
    with get_client() as client:
        return client.get(f"/users/{user_id}")


def get_current_user() -> dict:
    """Get currently authenticated user."""
    return get_user("me")


def create_user(
    email: str,
    login: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    password: Optional[str] = None,
    status: str = "invited",
    admin: bool = False
) -> dict:
    """Create or invite user.

    Args:
        email: User email (required)
        login: Login name (defaults to email prefix)
        first_name: First name
        last_name: Last name
        password: Password (required if status="active")
        status: "active" or "invited"
        admin: Grant admin privileges

    Returns:
        Created user dict
    """
    data = {
        "email": email,
        "login": login or email.split("@")[0],
        "status": status,
        "admin": admin
    }

    if first_name:
        data["firstName"] = first_name
    if last_name:
        data["lastName"] = last_name
    if password:
        data["password"] = password

    with get_client() as client:
        return client.post("/users", data)


def update_user(user_id: int, **updates) -> dict:
    """Update user.

    Updatable: email, login, firstName, lastName, admin
    """
    field_mapping = {
        "email": "email",
        "login": "login",
        "first_name": "firstName",
        "last_name": "lastName",
        "admin": "admin"
    }

    data = {}
    for arg, api_field in field_mapping.items():
        if arg in updates:
            data[api_field] = updates[arg]

    with get_client() as client:
        return client.patch(f"/users/{user_id}", data)


def delete_user(user_id: int) -> dict:
    """Delete user."""
    with get_client() as client:
        return client.delete(f"/users/{user_id}")


def lock_user(user_id: int) -> dict:
    """Lock user account."""
    with get_client() as client:
        return client.post(f"/users/{user_id}/lock")


def unlock_user(user_id: int) -> dict:
    """Unlock user account."""
    with get_client() as client:
        return client.delete(f"/users/{user_id}/lock")
