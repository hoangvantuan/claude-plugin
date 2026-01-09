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
| user | User ID or "me" |
| project | Project ID |
| work_package | Work package ID |
| spent_on | Date or range |
| activity | Activity type ID |
| created_at | Creation date |
| updated_at | Update date |

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
