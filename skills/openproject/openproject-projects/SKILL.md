---
name: openproject-projects
description: Manage OpenProject projects via API v3. Operations: list, create, get, update, delete, copy projects. Handle project hierarchy, versions, categories, types. Use when user needs to manage projects, create project structure, or query project data.
---

# OpenProject Projects

Manage projects in OpenProject.

## Prerequisites
- `openproject-core` skill loaded
- Environment: `OPENPROJECT_URL`, `OPENPROJECT_API_KEY`

## Scripts

### scripts/projects.py

Functions:
- `list_projects(filters, sort_by)` - List all projects
- `get_project(id)` - Get single project
- `create_project(name, **kwargs)` - Create new project
- `update_project(id, **kwargs)` - Update project
- `delete_project(id)` - Delete project
- `copy_project(id, new_name)` - Copy project
- `get_versions(project_id)` - List project versions
- `get_categories(project_id)` - List project categories

## Quick Examples

```python
from openproject_projects.projects import (
    list_projects, create_project, get_project
)

# List active projects
projects = list_projects(filters=[
    {"active": {"operator": "=", "values": ["t"]}}
])

# Create project
new_project = create_project(
    name="My Project",
    identifier="my-project",
    description="Project description"
)
```

## References
- `references/projects-api.md` - Full API details
- `references/project-filters.md` - Available filters
