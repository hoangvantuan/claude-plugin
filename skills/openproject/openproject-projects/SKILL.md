---
name: openproject-projects
description: Manage OpenProject projects via API v3. Operations: list, create, get, update, delete, copy projects. Handle project hierarchy, versions, categories, types. Use when user needs to manage projects, create project structure, or query project data.
---

# OpenProject Projects

Manage projects in OpenProject.

## Prerequisites
- Environment: `OPENPROJECT_URL`, `OPENPROJECT_API_KEY` in `.env`

## Package: `openproject_projects`

Functions:
- `list_projects(filters, sort_by)` - List all projects
- `get_project(id)` - Get single project by ID or identifier
- `create_project(name, **kwargs)` - Create new project
- `update_project(id, **kwargs)` - Update project
- `delete_project(id)` - Delete project
- `copy_project(id, new_name)` - Copy project
- `get_versions(project_id)` - List project versions
- `get_categories(project_id)` - List project categories
- `get_types(project_id)` - List available types
- `toggle_favorite(project_id, favorite)` - Star/unstar project

## Usage

**Always run from skill directory with `uv run`:**

```bash
cd .claude/skills/openproject
uv run python -c "YOUR_CODE"
```

### Examples

```python
from openproject_projects import (
    list_projects, create_project, get_project, get_versions
)
from dotenv import load_dotenv

load_dotenv()

# List active projects
for project in list_projects(filters=[
    {"active": {"operator": "=", "values": ["t"]}}
]):
    print(f"{project['id']}: {project['name']}")

# Create project
new_project = create_project(
    name="My Project",
    identifier="my-project",
    description="Project description",
    public=False
)

# Get project by identifier
project = get_project("my-project")

# Get versions
for version in get_versions(project["id"]):
    print(f"  {version['name']}")
```

## References
- `references/projects-api.md` - Full API details
