# OpenProject Skills

OpenProject API v3 integration skills for Claude Code.

## Configuration

Set environment variables:

```bash
export OPENPROJECT_URL="https://your-openproject-instance.com"
export OPENPROJECT_API_KEY="your-api-key-here"
```

Get your API key from: OpenProject > My Account > Access Tokens

## Skills

| Skill | Description |
|-------|-------------|
| `openproject-core` | Core utilities: HTTP client, HAL+JSON parsing, pagination, filters |
| `openproject-work-packages` | Manage tasks, issues, features. Relations, activities, watchers |
| `openproject-projects` | List, create, update, delete, copy projects. Versions, categories |
| `openproject-users` | Users, groups, memberships management |
| `openproject-time` | Time entries tracking and management |
| `openproject-notifications` | Read, mark as read notifications |
| `openproject-documents` | Documents, attachments, wiki pages |
| `openproject-queries` | Saved queries/views management |
| `openproject-admin` | System config, types, statuses, priorities, roles |

## Usage Examples

### List Open Work Packages

```python
from openproject_work_packages.work_packages import list_work_packages

wps = list_work_packages(filters=[
    {"status": {"operator": "o", "values": []}}
])
for wp in wps:
    print(f"#{wp['id']}: {wp['subject']}")
```

### Create Project

```python
from openproject_projects.projects import create_project

project = create_project(
    name="New Project",
    identifier="new-project",
    description="Project description"
)
```

### Track Time

```python
from openproject_time.time_entries import create_time_entry

entry = create_time_entry(
    work_package_id=123,
    hours=2.5,
    comment="Development work",
    activity_id=1
)
```

## Requirements

- Python >= 3.9
- httpx >= 0.24.0

## Setup with uv

```bash
# Create venv
uv venv --python 3.9
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

## Run Tests

```bash
uv run pytest skills/openproject/ -v
```
