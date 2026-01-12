# OpenProject API Basics

## Authentication

API Key via Basic Auth:
- Username: `apikey` (literal string)
- Password: Your API key

```python
# httpx example
client = httpx.Client(auth=("apikey", "your-api-key"))
```

## HAL+JSON Format

Responses use HAL+JSON with:
- `_type`: Resource type (e.g., "WorkPackage")
- `_links`: Related resources and actions
- `_embedded`: Embedded sub-resources

```json
{
  "_type": "WorkPackage",
  "id": 123,
  "subject": "Task title",
  "_links": {
    "self": {"href": "/api/v3/work_packages/123"},
    "project": {"href": "/api/v3/projects/1", "title": "My Project"}
  },
  "_embedded": {
    "status": {"_type": "Status", "id": 1, "name": "New"}
  }
}
```

## Pagination

Collection endpoints support:
- `offset`: Page number (1-based)
- `pageSize`: Items per page (default varies)

Response includes:
- `total`: Total items
- `count`: Items in current page
- `pageSize`: Page size used
- `offset`: Current offset

## Filters

JSON array format:
```json
[{ "field": { "operator": "=", "values": ["value1"] }}]
```

Common operators:
- `=`: Equals
- `!`: Not equals
- `~`: Contains
- `!~`: Not contains
- `o`: Open (status)
- `c`: Closed (status)
- `<d`: Before date
- `>d`: After date

Example: Open work packages in project 1
```json
[
  {"status": {"operator": "o", "values": []}},
  {"project": {"operator": "=", "values": ["1"]}}
]
```

## Sorting

JSON array format:
```json
[["field", "direction"], ["field2", "direction2"]]
```

Example: Sort by updated_at descending
```json
[["updatedAt", "desc"]]
```

## Error Format

```json
{
  "_type": "Error",
  "errorIdentifier": "urn:openproject-org:api:v3:errors:NotFound",
  "message": "The requested resource could not be found."
}
```

Common error identifiers:
- `urn:openproject-org:api:v3:errors:Unauthenticated` - Invalid/missing API key
- `urn:openproject-org:api:v3:errors:NotFound` - Resource not found
- `urn:openproject-org:api:v3:errors:InvalidQuery` - Bad query params
- `urn:openproject-org:api:v3:errors:PropertyConstraintViolation` - Validation error
