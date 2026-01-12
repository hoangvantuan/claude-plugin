---
name: openproject-time
description: Manage OpenProject time entries via API v3. Operations: list, create, update, delete time entries. Log work hours on work packages with activity types, comments. Supports filtering by user, project, work package, date range. Use when tracking time, generating time reports, or managing logged hours.
---

# OpenProject Time Tracking

Manage time entries in OpenProject.

## Prerequisites
- Environment: `OPENPROJECT_URL`, `OPENPROJECT_API_KEY` in `.env`
- Log time permission in project

## Package: `openproject_time`

**⚠️ IMPORTANT:** `list_time_entries()` returns a **generator**, not a list!
- Use `list()` to convert if you need `len()` or multiple iterations
- Example: `entries = list(list_time_entries(filters=...))`

**⚠️ IMPORTANT:** `hours` field returns **ISO 8601 duration**, not a number!
- Format: `PT1H30M45S` = 1 hour, 30 minutes, 45 seconds
- Use `parse_duration()` to convert to decimal hours
- Example: `parse_duration('PT1H30M') → 1.5`

**⚠️ IMPORTANT:** `get_work_packages_time()` returns **Dict**, not list!
- Return type: `Dict[int, List[dict]]` - key là WP ID, value là list entries
- Iterate with `.items()`: `for wp_id, entries in result.items()`

**⚠️ IMPORTANT:** `list_activities()` may return empty!
- Global activities often empty, activities are project-specific
- Use `openproject_work_packages.list_activities(wp_id)` for WP comments/history

Functions:
- `list_time_entries(filters)` - List with filters (returns generator)
- `get_time_entry(id)` - Get single entry
- `create_time_entry(work_package_id, hours, **kwargs)` - Log time
- `update_time_entry(id, **kwargs)` - Update entry
- `delete_time_entry(id)` - Delete entry
- `log_time(work_package_id, hours, **kwargs)` - Shortcut for create
- `list_activities()` - Get activity types
- `get_user_time_today(user_id)` - User's today entries
- `get_work_package_time(wp_id)` - Single WP's time entries (returns list)
- `get_work_packages_time(wp_ids)` - Multiple WPs, returns `Dict[int, List]` keyed by WP ID
- `parse_duration(str)` - Parse ISO 8601 duration to decimal hours

## Usage

**Always run from skill directory with `uv run`:**

```bash
cd .claude/skills/openproject
uv run python -c "YOUR_CODE"
```

### Examples

```python
from openproject_time import (
    log_time, list_time_entries, list_activities,
    get_user_time_today, parse_duration
)
from dotenv import load_dotenv

load_dotenv()

# Log 2 hours on work package
entry = log_time(
    work_package_id=123,
    hours=2.0,
    activity_id=1,  # Development
    comment="Implemented login feature",
    spent_on="2026-01-12"
)
print(f"Logged: {entry['id']}")

# List time entries and convert hours to decimal
for entry in list_time_entries(filters=[
    {"user": {"operator": "=", "values": ["me"]}},
    {"spent_on": {"operator": ">t-", "values": ["7"]}}
]):
    # hours is ISO 8601 duration (e.g., 'PT1H30M45S')
    hours = parse_duration(entry['hours'])
    print(f"{hours:.2f}h - {entry.get('comment', '')}")

# Get activity types
for activity in list_activities():
    print(activity["name"])

# Calculate total hours for today
total = sum(parse_duration(e['hours']) for e in get_user_time_today("me"))
print(f"Total today: {total:.2f}h")
```

## Lấy time entries theo Work Package

Dùng `entity_type` + `entity_id` filters (không phải `work_package`):

```python
from openproject_time import (
    get_work_package_time,      # Cho 1 WP
    get_work_packages_time,     # Cho nhiều WPs
    parse_duration
)

# Lấy time cho 1 work package
entries = get_work_package_time(wp_id=675)
hours = sum(parse_duration(e['hours']) for e in entries)
print(f"Total: {hours:.2f}h")

# Lấy time cho nhiều work packages (1 API call)
result = get_work_packages_time(wp_ids=[675, 598, 577])
for wp_id, entries in result.items():
    hours = sum(parse_duration(e['hours']) for e in entries)
    print(f"WP #{wp_id}: {hours:.2f}h")

# Hoặc filter trực tiếp
filters = [
    {"entity_type": {"operator": "=", "values": ["WorkPackage"]}},
    {"entity_id": {"operator": "=", "values": ["675", "598"]}}
]
entries = list(list_time_entries(filters=filters))
```

## References
- `references/time-api.md` - Full API details
