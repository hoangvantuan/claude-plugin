# Work Package Filters

## Common Filters

| Filter | Description |
|--------|-------------|
| status | Status ID, or "o" (open), "c" (closed) |
| project | Project ID |
| type | Type ID |
| assigned_to | Assignee user ID |
| author | Creator user ID |
| priority | Priority ID |
| version | Target version ID |

## Date Filters

| Filter | Values |
|--------|--------|
| created_at | ISO date range |
| updated_at | ISO date range |
| start_date | ISO date |
| due_date | ISO date |

## Relation Filters

| Filter | Description |
|--------|-------------|
| parent | Parent WP ID |
| blocks | WP that this blocks |
| blocked | WP that blocks this |
| precedes | WP that this precedes |
| follows | WP that this follows |

## Search Filters

| Filter | Description |
|--------|-------------|
| search | Full-text search |
| subject | Subject contains |
| description | Description contains |

## Operators

- `=` : equals
- `!` : not equals
- `o` : open (for status)
- `c` : closed (for status)
- `<>d` : between dates
- `>t-` : more than X days ago
- `<t+` : less than X days from now

## Examples

```python
# Open tasks assigned to user 5
[
  {"status": {"operator": "o", "values": []}},
  {"assigned_to": {"operator": "=", "values": ["5"]}}
]

# Overdue items
[
  {"due_date": {"operator": "<t+", "values": ["0"]}}
]

# Created this week
[
  {"created_at": {"operator": ">t-", "values": ["7"]}}
]
```
