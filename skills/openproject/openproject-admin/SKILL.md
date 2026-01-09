---
name: openproject-admin
description: OpenProject admin operations via API v3. Get system configuration. List/manage work package types, statuses, priorities, roles. Use when configuring system settings, managing type/status workflows, or checking instance configuration.
---

# OpenProject Admin

System administration and configuration.

## Prerequisites
- `openproject-core` skill loaded
- Admin permissions for some operations

## Scripts

### scripts/config.py
- `get_configuration()` - System configuration

### scripts/wp_types.py
- `list_types()` - Work package types
- `get_type(id)` - Type details

### scripts/statuses.py
- `list_statuses()` - All statuses
- `get_status(id)` - Status details

### scripts/roles.py
- `list_roles()` - All roles
- `get_role(id)` - Role with permissions

### scripts/priorities.py
- `list_priorities()` - All priorities
- `get_priority(id)` - Priority details

## Quick Examples

```python
from wp_types import list_types
from statuses import list_statuses
from roles import list_roles

# Get available work package types
for t in list_types():
    print(t["name"], t["color"])

# Get all statuses
for s in list_statuses():
    print(s["name"], "closed" if s["isClosed"] else "open")

# Get roles with permissions
for r in list_roles():
    print(r["name"])
```

## References
- `references/admin-api.md` - Full API details
