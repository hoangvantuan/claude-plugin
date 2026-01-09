# Projects API Reference

## Project Model

Key fields:
- `id`: Integer ID
- `identifier`: URL-friendly string
- `name`: Display name
- `description`: Rich text description
- `public`: Boolean
- `active`: Boolean
- `createdAt`, `updatedAt`: ISO timestamps

## Links

- `self`: Project URL
- `parent`: Parent project (if any)
- `categories`: Project categories
- `versions`: Project versions
- `types`: Enabled work package types
- `workPackages`: Work packages in project

## Create/Update Body

```json
{
  "name": "Project Name",
  "identifier": "project-name",
  "description": { "raw": "Description text" },
  "public": false,
  "_links": {
    "parent": { "href": "/api/v3/projects/1" }
  }
}
```

## Common Operations

### List with hierarchy
```python
# Get root projects only
list_projects(filters=[
    {"parent_id": {"operator": "!*", "values": []}}
])

# Get children of project 5
list_projects(filters=[
    {"parent_id": {"operator": "=", "values": ["5"]}}
])
```

### Sort projects
```python
# By name ascending
list_projects(sort_by=[("name", "asc")])

# By latest activity descending
list_projects(sort_by=[("latest_activity_at", "desc")])
```
