---
name: openproject-notifications
description: Manage OpenProject notifications via API v3. List, read, unread notifications. Handle in-app notifications (IAN). Use when managing notification state, building notification feeds, or automating notification handling.
---

# OpenProject Notifications

Manage in-app notifications (IAN).

## Prerequisites
- Environment: `OPENPROJECT_URL`, `OPENPROJECT_API_KEY` in `.env`

## Package: `openproject_notifications`

Functions:
- `list_notifications(filters)` - List notifications
- `get_notification(id)` - Get single notification
- `mark_read(id)` - Mark as read
- `mark_unread(id)` - Mark as unread
- `mark_all_read()` - Mark all as read
- `get_unread_count()` - Count unread
- `list_unread()` - List unread only
- `list_by_reason(reason)` - Filter by reason

## Usage

**Always run from skill directory with `uv run`:**

```bash
cd .claude/skills/openproject
uv run python -c "YOUR_CODE"
```

### Examples

```python
from openproject_notifications import (
    list_notifications, list_unread, mark_read, mark_all_read, get_unread_count
)
from dotenv import load_dotenv

load_dotenv()

# Get unread count
count = get_unread_count()
print(f"Unread: {count}")

# List unread notifications
for n in list_unread():
    print(f"{n['reason']}: {n['_links']['resource']['title']}")
    mark_read(n["id"])

# Or mark all as read
mark_all_read()

# List all notifications
for n in list_notifications():
    status = "read" if n.get("readIAN") else "unread"
    print(f"[{status}] {n['reason']}")
```

## References
- `references/notifications-api.md` - Full API details
