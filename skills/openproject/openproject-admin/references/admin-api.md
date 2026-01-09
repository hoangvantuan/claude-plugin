# Admin API Reference

## Configuration

Returns system settings:
- `perPageOptions`: Pagination options
- `dateFormat`: Date format string
- `timeFormat`: Time format string
- `startOfWeek`: Week start day
- `userPreferences`: User-specific settings

## Type Model

Key fields:
- `id`: Type ID
- `name`: Type name (Task, Bug, Feature)
- `color`: Hex color code
- `isDefault`: Default type flag
- `isMilestone`: Milestone flag
- `position`: Sort order

## Status Model

Key fields:
- `id`: Status ID
- `name`: Status name
- `color`: Hex color code
- `isClosed`: Closed status flag
- `isDefault`: Default status flag
- `position`: Sort order

## Role Model

Key fields:
- `id`: Role ID
- `name`: Role name
- `permissions`: List of permission strings

## Priority Model

Key fields:
- `id`: Priority ID
- `name`: Priority name
- `color`: Hex color code
- `isDefault`: Default priority flag
- `isActive`: Active flag
- `position`: Sort order

## Common Priorities

| ID | Name | Description |
|----|------|-------------|
| 7 | Immediate | Highest priority |
| 8 | Urgent | Very high |
| 9 | High | Above normal |
| 10 | Normal | Default |
| 11 | Low | Below normal |

## Endpoints

| Resource | Endpoint |
|----------|----------|
| Configuration | GET /configuration |
| Types | GET /types, GET /types/{id} |
| Statuses | GET /statuses, GET /statuses/{id} |
| Roles | GET /roles, GET /roles/{id} |
| Priorities | GET /priorities, GET /priorities/{id} |
