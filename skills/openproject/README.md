# OpenProject Skills

OpenProject API v3 integration skills for Claude Code.

## Quick Start

```bash
# 1. Navigate to skill directory
cd .claude/skills/openproject

# 2. Install dependencies
uv sync

# 3. Configure environment
cp .env.example .env
# Edit .env with your OpenProject URL and API key

# 4. Verify connection
uv run python -c "
from openproject_core import check_connection
from dotenv import load_dotenv
load_dotenv()
print(check_connection())
"
```

## Configuration

Create `.env` file with:

```bash
OPENPROJECT_URL=https://your-openproject-instance.com
OPENPROJECT_API_KEY=your-api-key-here
```

Get API key from: **OpenProject → My Account → Access Tokens**

## Package Structure

```
openproject/
├── openproject_core/        # Core client, auth, utilities
├── openproject_projects/    # Project CRUD operations
├── openproject_work_packages/  # Tasks, issues, relations
├── openproject_time/        # Time tracking
├── openproject_users/       # Users, groups, memberships
├── openproject_documents/   # Attachments, wiki
├── openproject_queries/     # Saved queries
├── openproject_notifications/  # Notifications
├── openproject_admin/       # System config
└── tests/                   # All tests
```

## Usage Examples

### Check Connection

```python
from openproject_core import check_connection
from dotenv import load_dotenv
load_dotenv()

status = check_connection()
print(f"Connected: {status['ok']}, User: {status['user']}")
```

### List Projects

```python
from openproject_projects import list_projects
from dotenv import load_dotenv
load_dotenv()

for project in list_projects():
    print(f"{project['id']}: {project['name']}")
```

### Create Work Package

```python
from openproject_work_packages import create_work_package
from dotenv import load_dotenv
load_dotenv()

wp = create_work_package(
    project_id=5,
    subject="New task",
    type_id=1,
    description="Task description"
)
print(f"Created: #{wp['id']}")
```

### Log Time

```python
from openproject_time import log_time
from dotenv import load_dotenv
load_dotenv()

entry = log_time(
    work_package_id=123,
    hours=2.5,
    comment="Development work"
)
```

### List Notifications

```python
from openproject_notifications import list_unread, get_unread_count
from dotenv import load_dotenv
load_dotenv()

print(f"Unread: {get_unread_count()}")
for n in list_unread():
    print(n['subject'])
```

## Running Scripts

**Always use `uv run` from the skill directory:**

```bash
cd .claude/skills/openproject

# One-liner
uv run python -c "from openproject_core import check_connection; print(check_connection())"

# Script file
uv run python my_script.py
```

## Run Tests

```bash
cd .claude/skills/openproject
uv run pytest -v
```

## Available Packages

| Package | Key Functions |
|---------|---------------|
| `openproject_core` | `check_connection()`, `OpenProjectClient`, `build_filters()`, `paginate()` |
| `openproject_projects` | `list_projects()`, `create_project()`, `update_project()`, `delete_project()` |
| `openproject_work_packages` | `list_work_packages()`, `create_work_package()`, `add_comment()`, `create_relation()` |
| `openproject_time` | `list_time_entries()`, `log_time()`, `get_work_package_time()`, `get_work_packages_time()` |
| `openproject_users` | `list_users()`, `create_user()`, `list_groups()`, `create_membership()` |
| `openproject_documents` | `upload_attachment()`, `download_attachment()`, `list_documents()` (read-only) |
| `openproject_queries` | `list_queries()`, `create_query()`, `star_query()` |
| `openproject_notifications` | `list_notifications()`, `mark_read()`, `get_unread_count()` |
| `openproject_admin` | `list_statuses()`, `list_priorities()`, `list_types()`, `list_roles()` |

## Important Notes

### Time Entries - Work Package Filter

API không hỗ trợ filter `work_package` trực tiếp. Dùng `entity_type` + `entity_id`:

```python
from openproject_time import get_work_package_time, get_work_packages_time

# Single WP
entries = get_work_package_time(wp_id=123)

# Multiple WPs (1 API call)
result = get_work_packages_time(wp_ids=[123, 456, 789])
```

### Documents API - Read Only

Documents API chỉ hỗ trợ **đọc**. Tạo/xóa documents phải qua web UI:

```python
from openproject_documents import list_documents, get_document

# List all documents (no project filter available)
for doc in list_documents():
    print(doc['title'])
```

### Attachments - Valid Container Types

```python
# ✓ Supported containers
"work_packages", "wiki_pages", "posts", "meetings", "activities"

# ✗ NOT supported
"documents"  # Use web UI instead
```
