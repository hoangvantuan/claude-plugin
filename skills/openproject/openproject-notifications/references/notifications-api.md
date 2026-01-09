# Notifications API Reference

## Notification Model

Key fields:
- `id`: Notification ID
- `reason`: Why notification was sent
- `readIAN`: Read status
- `createdAt`, `updatedAt`: Timestamps

## Links

- `self`: Notification URL
- `actor`: User who triggered notification
- `project`: Related project
- `resource`: Related resource (work package, etc.)
- `activity`: Activity that triggered notification

## Notification Reasons

| Reason | Description |
|--------|-------------|
| mentioned | Mentioned in comment |
| assigned | Assigned to work package |
| watched | Watching a work package |
| responsible | Accountable for work package |
| commented | Someone commented |
| created | Work package created |
| prioritized | Priority changed |
| scheduled | Date changed |
| dateAlert | Date approaching |

## Filters

| Filter | Values |
|--------|--------|
| readIAN | "t" (read), "f" (unread) |
| reason | See reasons above |
| project | Project ID |
| resourceType | "WorkPackage", etc. |

## Endpoints

| Method | Endpoint | Action |
|--------|----------|--------|
| GET | /notifications | List notifications |
| GET | /notifications/{id} | Get notification |
| POST | /notifications/{id}/read_ian | Mark as read |
| POST | /notifications/{id}/unread_ian | Mark as unread |
| POST | /notifications/read_ian | Mark all as read |

## Examples

```python
# Get unread mentions
[{"readIAN": {"operator": "=", "values": ["f"]}},
 {"reason": {"operator": "=", "values": ["mentioned"]}}]

# All project notifications
[{"project": {"operator": "=", "values": ["5"]}}]
```
