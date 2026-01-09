# Users API Reference

## User Model

Key fields:
- `id`: Integer ID
- `login`: Username
- `email`: Email address
- `firstName`, `lastName`: Name parts
- `name`: Full name (read-only)
- `status`: active, invited, locked
- `admin`: Boolean admin flag
- `createdAt`, `updatedAt`: Timestamps

## User Status Values

| Status | Description |
|--------|-------------|
| active | Active account |
| invited | Invited, pending activation |
| locked | Account locked |

## Create User

```json
{
  "email": "user@example.com",
  "login": "username",
  "firstName": "John",
  "lastName": "Doe",
  "password": "secret123",
  "status": "active",
  "admin": false
}
```

## Membership Model

```json
{
  "_links": {
    "project": { "href": "/projects/1" },
    "principal": { "href": "/principals/5" },
    "roles": [
      { "href": "/roles/3" },
      { "href": "/roles/4" }
    ]
  }
}
```

## Common Roles

| ID | Name | Typical Permissions |
|----|------|---------------------|
| 3 | Member | View, create, edit own |
| 4 | Manager | Full project access |
| 5 | Reader | View only |

## User Filters

```python
# Active users
[{"status": {"operator": "=", "values": ["active"]}}]

# Search by name
[{"name": {"operator": "~", "values": ["john"]}}]

# Users in group
[{"group": {"operator": "=", "values": ["5"]}}]
```
