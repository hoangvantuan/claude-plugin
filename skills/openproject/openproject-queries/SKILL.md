---
name: openproject-queries
description: Manage OpenProject saved queries via API v3. Create, update, delete saved queries (views). Build complex filters for work packages. Use when creating custom views, saving filter configurations, or automating query management.
---

# OpenProject Queries

Manage saved queries for work package views.

## Prerequisites
- `openproject-core` skill loaded

## Scripts

### scripts/queries.py
- `list_queries(project_id)` - List queries
- `get_query(id)` - Get query with filters
- `create_query(name, filters, **kwargs)` - Create query
- `update_query(id, **kwargs)` - Update query
- `delete_query(id)` - Delete query
- `star_query(id)` / `unstar_query(id)` - Favorites

## Quick Examples

```python
from queries import create_query, list_queries

# Create "My Open Tasks" query
query = create_query(
    name="My Open Tasks",
    project_id=5,
    filters=[
        {"status": {"operator": "o", "values": None}},
        {"assigned_to": {"operator": "=", "values": ["me"]}}
    ],
    columns=["id", "subject", "status", "priority", "dueDate"]
)

# List project queries
for q in list_queries(project_id=5):
    print(q["name"])
```

## References
- `references/queries-api.md` - Full API details
