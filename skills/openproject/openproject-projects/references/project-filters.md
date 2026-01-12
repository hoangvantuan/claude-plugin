# Project Filters Reference

## Available Filters

| Filter | Operators | Description |
|--------|-----------|-------------|
| active | =, ! | Project active status |
| ancestor | = | Projects under ancestor |
| id | =, ! | Project ID |
| name_and_identifier | ~ | Search name/identifier |
| parent_id | =, !, !* | Parent project |
| principal | = | Projects with member |
| type_id | = | Projects with type enabled |
| visible | = | Projects visible to user |

## Operators

- `=` : equals
- `!` : not equals
- `~` : contains
- `!~` : not contains
- `!*` : is null/empty

## Examples

```python
# Active projects
[{"active": {"operator": "=", "values": ["t"]}}]

# Search by name
[{"name_and_identifier": {"operator": "~", "values": ["marketing"]}}]

# Root projects (no parent)
[{"parent_id": {"operator": "!*", "values": []}}]

# Combined
[
  {"active": {"operator": "=", "values": ["t"]}},
  {"name_and_identifier": {"operator": "~", "values": ["dev"]}}
]
```
