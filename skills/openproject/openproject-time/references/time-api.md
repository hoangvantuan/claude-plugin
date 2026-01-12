# Time Entries API Reference

## Time Entry Model

Key fields:
- `id`: Entry ID
- `hours`: ISO duration (PT2H = 2 hours)
- `spentOn`: Date (YYYY-MM-DD)
- `comment`: Work description
- `createdAt`, `updatedAt`: Timestamps

## Links

- `self`: Entry URL
- `workPackage`: Associated work package
- `project`: Project
- `user`: User who logged time
- `activity`: Activity type

## Filters

| Filter | Description |
|--------|-------------|
| entity_type | "WorkPackage" or "Meeting" |
| entity_id | Entity IDs (work package/meeting) |
| project_id | Project ID |
| user_id | User ID |
| spent_on | Date or range |
| activity_id | Activity type ID |
| ongoing | Filter ongoing timers |
| created_at | Creation date |
| updated_at | Update date |

**Filter theo Work Package:**

```python
from openproject_time import get_work_package_time, get_work_packages_time

# Cho 1 WP
entries = get_work_package_time(wp_id=675)

# Cho nhiều WPs (1 API call)
result = get_work_packages_time(wp_ids=[675, 598, 577])

# Hoặc dùng filter trực tiếp
filters = [
    {"entity_type": {"operator": "=", "values": ["WorkPackage"]}},
    {"entity_id": {"operator": "=", "values": ["675", "598"]}}
]
entries = list(list_time_entries(filters=filters))
```

## Date Filter Operators

- `=` : exact date
- `<>d` : between dates
- `>t-` : more than X days ago
- `<t+` : less than X days from now
- `t` : today
- `w` : this week

## Examples

```python
# This week's entries
[{"spent_on": {"operator": "w", "values": None}}]

# Last 30 days
[{"spent_on": {"operator": ">t-", "values": ["30"]}}]

# Date range
[{"spent_on": {"operator": "<>d", "values": ["2026-01-01", "2026-01-31"]}}]
```

## Duration Format

Hours use ISO 8601 duration:
- `PT1H` = 1 hour
- `PT1H30M` = 1.5 hours
- `PT2H` = 2 hours

API accepts decimal hours in create/update, returns ISO duration.
