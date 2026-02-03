"""OpenProject Project Config - Cache project metadata to reduce API calls."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional, TypedDict

import yaml

from .client import OpenProjectClient
from .helpers import paginate

CONFIG_FILENAME = ".openproject-config.yml"


class ProjectConfig(TypedDict):
    """Project configuration structure."""
    generated_at: str
    updated_at: str
    instance: dict
    project: dict
    members: list
    types: list
    statuses: list
    priorities: list
    versions: list
    categories: list
    custom_fields: dict


def get_config_path() -> Path:
    """Get config file path (skill directory root)."""
    skill_dir = Path(__file__).parent.parent.parent
    return skill_dir / CONFIG_FILENAME


def is_config_initialized() -> bool:
    """Check if config file exists and is valid."""
    config_path = get_config_path()
    if not config_path.exists():
        return False
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config is not None and "project" in config
    except (yaml.YAMLError, IOError):
        return False


def load_config() -> Optional[ProjectConfig]:
    """Load config from YAML file.

    Returns:
        ProjectConfig dict or None if not initialized
    """
    if not is_config_initialized():
        return None
    config_path = get_config_path()
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_config(config: ProjectConfig) -> None:
    """Save config to YAML file."""
    config_path = get_config_path()
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(
            config,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120
        )


def _fetch_instance_info(client: OpenProjectClient) -> dict:
    """Fetch current user and instance info."""
    me = client.get("/users/me")
    return {
        "url": client.base_url,
        "user_id": me.get("id"),
        "user_name": f"{me.get('firstName', '')} {me.get('lastName', '')}".strip(),
        "user_login": me.get("login"),
        "user_email": me.get("email"),
        "is_admin": me.get("admin", False)
    }


def _fetch_project_info(client: OpenProjectClient, project_id: int) -> dict:
    """Fetch project details."""
    project = client.get(f"/projects/{project_id}")
    return {
        "id": project.get("id"),
        "identifier": project.get("identifier"),
        "name": project.get("name"),
        "description": project.get("description", {}).get("raw", ""),
        "active": project.get("active", True),
        "public": project.get("public", False)
    }


def _fetch_members(client: OpenProjectClient, project_id: int) -> list:
    """Fetch project members via memberships."""
    members = []
    for membership in paginate(client, "/memberships", params={
        "filters": f'[{{"project":{{"operator":"=","values":["{project_id}"]}}}}]'
    }):
        principal = membership.get("_links", {}).get("principal", {})
        principal_href = principal.get("href", "")
        principal_title = principal.get("title", "")

        roles = []
        for role_link in membership.get("_links", {}).get("roles", []):
            roles.append({
                "href": role_link.get("href", ""),
                "title": role_link.get("title", "")
            })

        members.append({
            "membership_id": membership.get("id"),
            "principal_href": principal_href,
            "principal_name": principal_title,
            "roles": roles
        })
    return members


def _fetch_types(client: OpenProjectClient, project_id: int) -> list:
    """Fetch project-specific work package types."""
    types = []
    for t in paginate(client, f"/projects/{project_id}/types"):
        types.append({
            "id": t.get("id"),
            "name": t.get("name"),
            "color": t.get("color"),
            "is_milestone": t.get("isMilestone", False)
        })
    return types


def _fetch_statuses(client: OpenProjectClient) -> list:
    """Fetch all statuses."""
    statuses = []
    for s in paginate(client, "/statuses"):
        statuses.append({
            "id": s.get("id"),
            "name": s.get("name"),
            "color": s.get("color"),
            "is_closed": s.get("isClosed", False),
            "is_default": s.get("isDefault", False),
            "position": s.get("position")
        })
    return sorted(statuses, key=lambda x: x.get("position", 0))


def _fetch_priorities(client: OpenProjectClient) -> list:
    """Fetch all priorities."""
    priorities = []
    for p in paginate(client, "/priorities"):
        priorities.append({
            "id": p.get("id"),
            "name": p.get("name"),
            "color": p.get("color"),
            "is_default": p.get("isDefault", False),
            "position": p.get("position")
        })
    return sorted(priorities, key=lambda x: x.get("position", 0))


def _fetch_versions(client: OpenProjectClient, project_id: int) -> list:
    """Fetch project versions."""
    versions = []
    for v in paginate(client, f"/projects/{project_id}/versions"):
        versions.append({
            "id": v.get("id"),
            "name": v.get("name"),
            "status": v.get("status"),
            "start_date": v.get("startDate"),
            "end_date": v.get("endDate"),
            "description": v.get("description", {}).get("raw", "")
        })
    return versions


def _fetch_categories(client: OpenProjectClient, project_id: int) -> list:
    """Fetch project categories."""
    categories = []
    for c in paginate(client, f"/projects/{project_id}/categories"):
        categories.append({
            "id": c.get("id"),
            "name": c.get("name")
        })
    return categories


def _fetch_custom_fields(client: OpenProjectClient, project_id: int, type_ids: list) -> dict:
    """Fetch custom fields for each type via schema."""
    custom_fields = {}
    for type_id in type_ids:
        try:
            schema = client.get(f"/work_packages/schemas/{project_id}-{type_id}")
            fields = {}
            for key, val in schema.items():
                if key.startswith("customField") and isinstance(val, dict):
                    fields[key] = {
                        "name": val.get("name"),
                        "type": val.get("type"),
                        "required": val.get("required", False),
                        "writable": val.get("writable", True)
                    }
            if fields:
                custom_fields[str(type_id)] = fields
        except Exception:
            continue
    return custom_fields


def init_config(project_id: int) -> ProjectConfig:
    """Initialize config by fetching all project metadata.

    Args:
        project_id: OpenProject project ID (numeric)

    Returns:
        ProjectConfig dict with all fetched data
    """
    with OpenProjectClient() as client:
        now = datetime.now().isoformat()

        instance = _fetch_instance_info(client)
        project = _fetch_project_info(client, project_id)
        members = _fetch_members(client, project_id)
        types = _fetch_types(client, project_id)
        statuses = _fetch_statuses(client)
        priorities = _fetch_priorities(client)
        versions = _fetch_versions(client, project_id)
        categories = _fetch_categories(client, project_id)

        type_ids = [t["id"] for t in types]
        custom_fields = _fetch_custom_fields(client, project_id, type_ids)

        config: ProjectConfig = {
            "generated_at": now,
            "updated_at": now,
            "instance": instance,
            "project": project,
            "members": members,
            "types": types,
            "statuses": statuses,
            "priorities": priorities,
            "versions": versions,
            "categories": categories,
            "custom_fields": custom_fields
        }

        save_config(config)
        return config


def refresh_config() -> Optional[ProjectConfig]:
    """Refresh config by re-fetching all data.

    Returns:
        Updated ProjectConfig or None if not initialized
    """
    current = load_config()
    if not current or "project" not in current:
        return None

    project_id = current["project"]["id"]
    return init_config(project_id)


def require_config() -> ProjectConfig:
    """Load config or raise error if not initialized.

    Returns:
        ProjectConfig

    Raises:
        RuntimeError: If config not initialized
    """
    config = load_config()
    if not config:
        raise RuntimeError(
            "OpenProject config not initialized!\n"
            "Run init_config(project_id) first or use the command:\n"
            "  cd skills/openproject && uv run python -c \"\n"
            "from openproject_core import init_config\n"
            "from dotenv import load_dotenv\n"
            "load_dotenv()\n"
            "init_config(PROJECT_ID)  # Replace with your project ID\n"
            "\""
        )
    return config


def get_project_id() -> Optional[int]:
    """Get configured project ID."""
    config = load_config()
    if config and "project" in config:
        return config["project"].get("id")
    return None


def get_type_id(type_name: str) -> Optional[int]:
    """Get type ID by name from config."""
    config = load_config()
    if not config:
        return None
    for t in config.get("types", []):
        if t["name"].lower() == type_name.lower():
            return t["id"]
    return None


def get_status_id(status_name: str) -> Optional[int]:
    """Get status ID by name from config."""
    config = load_config()
    if not config:
        return None
    for s in config.get("statuses", []):
        if s["name"].lower() == status_name.lower():
            return s["id"]
    return None


def get_priority_id(priority_name: str) -> Optional[int]:
    """Get priority ID by name from config."""
    config = load_config()
    if not config:
        return None
    for p in config.get("priorities", []):
        if p["name"].lower() == priority_name.lower():
            return p["id"]
    return None


def get_version_id(version_name: str) -> Optional[int]:
    """Get version ID by name from config."""
    config = load_config()
    if not config:
        return None
    for v in config.get("versions", []):
        if v["name"].lower() == version_name.lower():
            return v["id"]
    return None


def get_custom_field_name(field_key: str, type_id: int) -> Optional[str]:
    """Get custom field human-readable name.

    Args:
        field_key: e.g. "customField10"
        type_id: Work package type ID

    Returns:
        Field name or None
    """
    config = load_config()
    if not config:
        return None
    type_fields = config.get("custom_fields", {}).get(str(type_id), {})
    field_info = type_fields.get(field_key, {})
    return field_info.get("name")


def print_config_summary() -> None:
    """Print human-readable config summary."""
    config = load_config()
    if not config:
        print("Config not initialized!")
        return

    print(f"=== OpenProject Config ===")
    print(f"Generated: {config.get('generated_at')}")
    print(f"Updated: {config.get('updated_at')}")
    print()

    inst = config.get("instance", {})
    print(f"Instance: {inst.get('url')}")
    print(f"User: {inst.get('user_name')} ({inst.get('user_login')})")
    print()

    proj = config.get("project", {})
    print(f"Project: {proj.get('name')} (ID: {proj.get('id')})")
    print(f"Identifier: {proj.get('identifier')}")
    print()

    print(f"Members: {len(config.get('members', []))}")
    print(f"Types: {len(config.get('types', []))}")
    print(f"Statuses: {len(config.get('statuses', []))}")
    print(f"Priorities: {len(config.get('priorities', []))}")
    print(f"Versions: {len(config.get('versions', []))}")
    print(f"Categories: {len(config.get('categories', []))}")

    cf_count = sum(len(v) for v in config.get("custom_fields", {}).values())
    print(f"Custom Fields: {cf_count} (across {len(config.get('custom_fields', {}))} types)")


def load_session_config() -> dict:
    """Load config and return session summary for verification.

    MUST be called at the start of every work session!

    Returns:
        dict with session info:
        - ok: bool - Config loaded successfully
        - project: str - Project name
        - project_id: int - Project ID
        - user: str - Current user name
        - instance: str - OpenProject URL
        - updated_at: str - Last config update time
        - error: str - Error message if not ok

    Example:
        >>> session = load_session_config()
        >>> if not session['ok']:
        ...     print(f"ERROR: {session['error']}")
        ... else:
        ...     print(f"Session ready: {session['project']} (ID: {session['project_id']})")
    """
    if not is_config_initialized():
        return {
            "ok": False,
            "error": "Config not initialized! Run init_config(project_id) first."
        }

    config = load_config()
    if not config:
        return {
            "ok": False,
            "error": "Failed to load config file."
        }

    proj = config.get("project", {})
    inst = config.get("instance", {})

    return {
        "ok": True,
        "project": proj.get("name", "Unknown"),
        "project_id": proj.get("id"),
        "identifier": proj.get("identifier"),
        "user": inst.get("user_name", "Unknown"),
        "user_login": inst.get("user_login"),
        "instance": inst.get("url", "Unknown"),
        "updated_at": config.get("updated_at"),
        "types_count": len(config.get("types", [])),
        "members_count": len(config.get("members", [])),
    }
