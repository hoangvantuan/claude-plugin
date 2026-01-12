---
name: openproject-admin
description: OpenProject admin operations via API v3. Get system configuration. List/manage work package types, statuses, priorities, roles. Use when configuring system settings, managing type/status workflows, or checking instance configuration.
---

# OpenProject Admin

System administration and configuration.

## Prerequisites
- Environment: `OPENPROJECT_URL`, `OPENPROJECT_API_KEY` in `.env`
- Admin permissions for some operations

## Package: `openproject_admin`

### Configuration
- `get_configuration()` - System configuration

### Types
- `list_types()` - Work package types
- `get_type(id)` - Type details
- `list_project_types(project_id)` - Project-specific types

### Statuses
- `list_statuses()` - All statuses
- `get_status(id)` - Status details
- `list_open_statuses()` - Open statuses only
- `list_closed_statuses()` - Closed statuses only

### Priorities
- `list_priorities()` - All priorities
- `get_priority(id)` - Priority details
- `get_default_priority()` - Default priority

### Roles
- `list_roles()` - All roles
- `get_role(id)` - Role with permissions

## Usage

**Always run from skill directory with `uv run`:**

```bash
cd .claude/skills/openproject
uv run python -c "YOUR_CODE"
```

### Examples

```python
from openproject_admin import (
    get_configuration,
    list_types, list_statuses, list_priorities, list_roles,
    list_open_statuses, get_default_priority
)
from dotenv import load_dotenv

load_dotenv()

# Get system configuration
config = get_configuration()
print(f"Version: {config.get('coreVersion')}")

# Get available work package types
for t in list_types():
    print(f"{t['name']} - {t.get('color', 'no color')}")

# Get all statuses
for s in list_statuses():
    status_type = "closed" if s["isClosed"] else "open"
    print(f"{s['name']} ({status_type})")

# Get only open statuses
for s in list_open_statuses():
    print(f"Open: {s['name']}")

# Get default priority
default = get_default_priority()
print(f"Default priority: {default['name']}")

# Get roles with permissions
for r in list_roles():
    print(f"{r['name']}")
```

## References
- `references/admin-api.md` - Full API details
