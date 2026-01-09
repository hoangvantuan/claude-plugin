---
name: openproject-time
description: Manage OpenProject time entries via API v3. Operations: list, create, update, delete time entries. Log work hours on work packages with activity types, comments. Supports filtering by user, project, work package, date range. Use when tracking time, generating time reports, or managing logged hours.
---

# OpenProject Time Tracking

Manage time entries in OpenProject.

## Prerequisites
- `openproject-core` skill loaded
- Log time permission in project

## Scripts

### scripts/time_entries.py
- `list_time_entries(filters)` - List with filters
- `get_time_entry(id)` - Get single entry
- `create_time_entry(work_package_id, hours, **kwargs)` - Log time
- `update_time_entry(id, **kwargs)` - Update entry
- `delete_time_entry(id)` - Delete entry
- `list_activities()` - Get activity types
- `log_time()` - Alias for create
- `get_user_time_today()` - Today's entries
- `get_work_package_time()` - WP's entries

## Quick Examples

```python
from time_entries import create_time_entry, list_time_entries

# Log 2 hours on work package
entry = create_time_entry(
    work_package_id=123,
    hours=2.0,
    activity_id=1,  # Development
    comment="Implemented login feature",
    spent_on="2026-01-09"
)

# List time entries for user this week
entries = list_time_entries(filters=[
    {"user": {"operator": "=", "values": ["me"]}},
    {"spent_on": {"operator": ">t-", "values": ["7"]}}
])
```

## References
- `references/time-api.md` - Full API details
