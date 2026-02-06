---
name: openproject-queries
description: Manage OpenProject saved queries via API v3. Create, update, delete saved queries (views). Build complex filters for work packages. Use when creating custom views, saving filter configurations, or automating query management.
---

# OpenProject Queries

Manage saved queries for work package views.

## Prerequisites

* Environment: `OPENPROJECT_URL`, `OPENPROJECT_API_KEY` in `.env`

## Package: `openproject_queries`

Functions:

* `list_queries(project_id)` - List queries

* `get_query(id)` - Get query with filters

* `create_query(name, filters, **kwargs)` - Create query

* `update_query(id, **kwargs)` - Update query

* `delete_query(id)` - Delete query

* `star_query(id)` / `unstar_query(id)` - Manage favorites

* `get_query_default(project_id)` - Get default query

* `get_available_columns()` - Get column options

## Usage

**Always run from skill directory with** **`uv run`:**

```bash
cd .claude/skills/openproject
uv run python -c "YOUR_CODE"
```

### Examples

```python
from openproject_queries import (
    list_queries, create_query, star_query, get_available_columns
)
from dotenv import load_dotenv

load_dotenv()

# List project queries
for query in list_queries(project_id=5):
    print(f"{query['id']}: {query['name']}")

# Create "My Open Tasks" query
query = create_query(
    name="My Open Tasks",
    project_id=5,
    filters=[
        {"status": {"operator": "o", "values": []}},
        {"assignee": {"operator": "=", "values": ["me"]}}
    ],
    columns=["id", "subject", "status", "priority", "dueDate"]
)

# Star the query
star_query(query["id"])

# Get available columns
for col in get_available_columns():
    print(col["id"])
```

## References

* `references/queries-api.md` - Full API details

