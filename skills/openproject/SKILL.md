---
name: openproject
description: OpenProject API v3 integration for project management. Manage projects, work packages, time entries, documents, users, notifications, queries. Use when user needs to interact with OpenProject instance - create/update work packages, track time, manage projects, query data, handle documents and attachments.
---

# OpenProject Integration

Full OpenProject API v3 integration with Python scripts.

## Setup

1. Set environment variables in `.claude/skills/openproject/.env`:
   - `OPENPROJECT_URL`: OpenProject instance URL
   - `OPENPROJECT_API_KEY`: API key from My Account

2. Install dependencies:
```bash
pip install -r openproject-core/requirements.txt
```

## Sub-Skills

| Skill | Purpose |
|-------|---------|
| `openproject-core` | Base client, auth, HAL parsing, pagination |
| `openproject-projects` | List, create, update, delete projects |
| `openproject-work-packages` | Manage work packages (tasks, bugs, features) |
| `openproject-time` | Time entries logging and reporting |
| `openproject-users` | Users, groups, memberships |
| `openproject-documents` | Documents, wiki, attachments |
| `openproject-queries` | Saved queries and views |
| `openproject-notifications` | User notifications |
| `openproject-admin` | System config, types, statuses, roles |

## Quick Start

```python
# Initialize client
from openproject_core.client import OpenProjectClient
client = OpenProjectClient()

# List projects
from openproject_projects.projects import list_projects
projects = list_projects()

# Create work package
from openproject_work_packages.work_packages import create_work_package
wp = create_work_package(project_id=1, subject="New task", type_id=1)

# Log time
from openproject_time.time_entries import create_time_entry
entry = create_time_entry(work_package_id=123, hours=2.5, comment="Development")

client.close()
```

## Common Tasks

- **Create task**: Use `openproject-work-packages`
- **Track time**: Use `openproject-time`
- **Manage projects**: Use `openproject-projects`
- **Upload files**: Use `openproject-documents`
- **Query data**: Use `openproject-queries`

## References
- Each sub-skill has detailed `references/*.md` files
- `spec.yml` - Full OpenAPI specification
