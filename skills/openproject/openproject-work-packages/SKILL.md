---
name: openproject-work-packages
description: Manage OpenProject work packages via API v3. Operations: list, create, update, delete work packages. Handle relations (blocks, follows, parent), activities (comments, history), watchers. Supports 40+ filter types. Use when managing tasks, issues, features, or any work items.
---

# OpenProject Work Packages

Manage work packages (tasks, issues, features) in OpenProject.

## Prerequisites
- `openproject-core` skill loaded
- Environment variables configured

## Scripts

### scripts/work_packages.py
- `list_work_packages(filters, sort_by)` - List with filters
- `get_work_package(id)` - Get single WP
- `create_work_package(project_id, subject, **kwargs)` - Create WP
- `update_work_package(id, **kwargs)` - Update WP
- `delete_work_package(id)` - Delete WP

### scripts/activities.py
- `list_activities(wp_id)` - Get comments/history
- `add_comment(wp_id, comment)` - Add comment

### scripts/relations.py
- `list_relations(wp_id)` - Get relations
- `create_relation(from_id, to_id, type)` - Create relation
- `delete_relation(relation_id)` - Remove relation

## Quick Examples

```python
from openproject_work_packages.work_packages import (
    list_work_packages, create_work_package
)

# List open work packages in project
wps = list_work_packages(filters=[
    {"project": {"operator": "=", "values": ["5"]}},
    {"status": {"operator": "o", "values": []}}
])

# Create task
wp = create_work_package(
    project_id=5,
    subject="Implement login",
    type_id=1,
    description="Add OAuth2 login"
)
```

## References
- `references/work-packages-api.md` - API details
- `references/wp-filters.md` - 40+ filters
- `references/relations-types.md` - Relation types
