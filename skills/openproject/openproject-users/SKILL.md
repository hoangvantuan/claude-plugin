---
name: openproject-users
description: Manage OpenProject users, groups, and memberships via API v3. Operations: list/create/update/delete users, manage groups and group members, assign project memberships with roles. Use when managing team access, user accounts, or project permissions.
---

# OpenProject Users

Manage users, groups, and project memberships.

## Prerequisites
- Environment: `OPENPROJECT_URL`, `OPENPROJECT_API_KEY` in `.env`
- Admin permissions for most operations

## Package: `openproject_users`

### Users
- `list_users(filters)` - List users
- `get_user(id)` - Get user details
- `get_current_user()` - Get current user
- `create_user(email, **kwargs)` - Create/invite user
- `update_user(id, **kwargs)` - Update user
- `delete_user(id)` - Delete user
- `lock_user(id)` / `unlock_user(id)` - Lock status

### Groups
- `list_groups()` - List all groups
- `get_group(id)` - Get group details
- `create_group(name)` - Create group
- `add_member(group_id, user_id)` - Add user to group
- `remove_member(group_id, user_id)` - Remove from group

### Memberships
- `list_memberships(project_id)` - Project members
- `create_membership(project_id, principal_id, role_ids)` - Add member
- `delete_membership(id)` - Remove member

## Usage

**Always run from skill directory with `uv run`:**

```bash
cd .claude/skills/openproject
uv run python -c "YOUR_CODE"
```

### Examples

```python
from openproject_users import (
    list_users, create_user, get_current_user,
    list_groups, create_group, add_member,
    list_memberships, create_membership
)
from dotenv import load_dotenv

load_dotenv()

# Get current user
me = get_current_user()
print(f"Logged in as: {me['name']}")

# List users
for user in list_users():
    print(f"{user['id']}: {user['name']} ({user['login']})")

# Invite user
user = create_user(
    email="new@example.com",
    login="newuser",
    firstName="New",
    lastName="User",
    status="invited"
)

# Add to project with role
create_membership(
    project_id=5,
    principal_id=user["id"],
    role_ids=[3]  # Member role
)

# Create group and add member
group = create_group("Development Team")
add_member(group["id"], user["id"])
```

## References
- `references/users-api.md` - Full API details
