---
name: openproject-work-packages
description: Manage OpenProject work packages via API v3. Operations: list, create, update, delete work packages. Handle relations (blocks, follows, parent), activities (comments, history), watchers. Supports 40+ filter types. Use when managing tasks, issues, features, or any work items.
---

# OpenProject Work Packages

Manage work packages (tasks, issues, features) in OpenProject.

## Prerequisites
- Environment: `OPENPROJECT_URL`, `OPENPROJECT_API_KEY` in `.env`

## Package: `openproject_work_packages`

### Work Packages
- `list_work_packages(filters, sort_by)` - List with filters
- `get_work_package(id)` - Get single WP
- `create_work_package(project_id, subject, **kwargs)` - Create WP
- `update_work_package(id, **kwargs)` - Update WP
- `delete_work_package(id)` - Delete WP
- `get_schema(project_id, type_id)` - Get form schema (BOTH params required!)

**⚠️ IMPORTANT:** `get_schema()` requires BOTH `project_id` AND `type_id`!
- Common types: `1` = Task, `6` = User Story, `10` = TechDebt
- Use to discover custom field names (vary by project/type)

### Activities
- `list_activities(wp_id)` - Get comments/history
- `add_comment(wp_id, comment)` - Add comment

### Relations
- `list_relations(wp_id)` - Get relations
- `create_relation(from_id, to_id, type, description, delay)` - Create relation
- `get_relation(relation_id)` - Get relation details
- `delete_relation(relation_id)` - Remove relation

**Relation types:** `relates`, `duplicates`, `duplicated`, `blocks`, `blocked`, `precedes`, `follows`, `includes`, `partof`, `requires`, `required`

**Note:** `delay` parameter maps to API's `lag` field (days between WPs for precedes/follows)

## Usage

**Always run from skill directory with `uv run`:**

```bash
cd .claude/skills/openproject
uv run python -c "YOUR_CODE"
```

### Examples

```python
from openproject_work_packages import (
    list_work_packages, create_work_package, add_comment, create_relation
)
from dotenv import load_dotenv

load_dotenv()

# List open work packages in project
for wp in list_work_packages(filters=[
    {"project": {"operator": "=", "values": ["5"]}},
    {"status": {"operator": "o", "values": []}}
]):
    print(f"#{wp['id']}: {wp['subject']}")

# Create task
wp = create_work_package(
    project_id=5,
    subject="Implement login",
    type_id=1,
    description="Add OAuth2 login"
)

# Add comment
add_comment(wp["id"], "Started working on this")

# Create relation (blocks)
create_relation(from_id=wp["id"], to_id=124, relation_type="blocks")
```

### Get Custom Field Names

```python
from openproject_work_packages import get_schema, list_work_packages
from dotenv import load_dotenv

load_dotenv()

# Get schema to discover custom field mapping
schema = get_schema(project_id=3, type_id=6)  # project 3, User Story

# Extract custom field names
cf_names = {}
for key, val in schema.items():
    if key.startswith('customField') and isinstance(val, dict):
        cf_names[key] = val.get('name')
        print(f"{key}: {val.get('name')}")

# Output:
# customField10: Research Point
# customField8: Excute Point
# customField9: Verify Point
# customField15: Review Point

# Then access in work packages
for wp in list_work_packages(project_id=3):
    research = wp.get('customField10') or 0
    execute = wp.get('customField8') or 0
    print(f"#{wp['id']}: Research={research}, Execute={execute}")
```

## References
- `references/work-packages-api.md` - API details
- `references/wp-filters.md` - 40+ filters
- `references/relations-types.md` - Relation types
