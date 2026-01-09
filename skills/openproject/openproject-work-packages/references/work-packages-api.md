# Work Packages API Reference

## Work Package Model

Key fields:
- `id`: Integer ID
- `subject`: Title
- `description`: Rich text (format: markdown, raw, html)
- `startDate`, `dueDate`: ISO dates
- `estimatedTime`: ISO 8601 duration (e.g., "PT8H")
- `percentageDone`: 0-100
- `createdAt`, `updatedAt`: ISO timestamps

## Links

- `self`: Work package URL
- `project`: Parent project
- `type`: WP type (Task, Bug, Feature)
- `status`: Current status
- `priority`: Priority level
- `assignee`: Assigned user
- `responsible`: Responsible user
- `parent`: Parent work package

## Create/Update Body

```json
{
  "subject": "Task title",
  "description": { "raw": "Description text" },
  "startDate": "2024-01-15",
  "dueDate": "2024-01-20",
  "_links": {
    "project": { "href": "/projects/1" },
    "type": { "href": "/types/1" },
    "status": { "href": "/statuses/1" },
    "assignee": { "href": "/users/5" }
  }
}
```

## Duration Format

Estimated time uses ISO 8601 duration:
- `PT1H` = 1 hour
- `PT8H` = 8 hours
- `PT1H30M` = 1.5 hours
