---
name: openproject-notifications
description: Manage OpenProject notifications via API v3. List, read, unread notifications. Handle in-app notifications (IAN). Use when managing notification state, building notification feeds, or automating notification handling.
---

# OpenProject Notifications

Manage in-app notifications (IAN).

## Prerequisites
- `openproject-core` skill loaded

## Scripts

### scripts/notifications.py
- `list_notifications(filters)` - List notifications
- `get_notification(id)` - Get single notification
- `mark_read(id)` - Mark as read
- `mark_unread(id)` - Mark as unread
- `mark_all_read()` - Mark all as read
- `get_unread_count()` - Count unread

## Quick Examples

```python
from notifications import list_notifications, mark_read, mark_all_read

# Get unread notifications
for n in list_notifications(read_status=False):
    print(n["reason"], n["_links"]["resource"]["title"])
    mark_read(n["id"])

# Mark all as read
mark_all_read()
```

## References
- `references/notifications-api.md` - Full API details
