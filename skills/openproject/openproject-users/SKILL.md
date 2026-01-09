---
name: openproject-users
description: Manage OpenProject users, groups, and memberships via API v3. Operations: list/create/update/delete users, manage groups and group members, assign project memberships with roles. Use when managing team access, user accounts, or project permissions.
---

# OpenProject Users

Manage users, groups, and project memberships.

## Prerequisites
- `openproject-core` skill loaded
- Admin permissions for most operations

## Scripts

### scripts/users.py
- `list_users(filters)` - List users
- `get_user(id)` - Get user details
- `create_user(email, **kwargs)` - Create/invite user
- `update_user(id, **kwargs)` - Update user
- `lock_user(id)` / `unlock_user(id)` - Lock status

### scripts/groups.py
- `list_groups()` - List all groups
- `create_group(name)` - Create group
- `add_member(group_id, user_id)` - Add user to group
- `remove_member(group_id, user_id)` - Remove from group

### scripts/memberships.py
- `list_memberships(project_id)` - Project members
- `create_membership(project_id, principal_id, role_ids)` - Add member
- `update_membership(id, role_ids)` - Change roles
- `delete_membership(id)` - Remove member

## Quick Examples

```python
from openproject_users.users import list_users, create_user
from openproject_users.memberships import create_membership

# Invite user
user = create_user(
    email="new@example.com",
    status="invited"
)

# Add to project with role
create_membership(
    project_id=5,
    principal_id=user["id"],
    role_ids=[3]  # Member role
)
```

## References
- `references/users-api.md` - Full API details
