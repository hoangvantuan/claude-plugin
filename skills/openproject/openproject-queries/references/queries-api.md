# Queries API Reference

## Query Model

Key fields:
- `id`: Query ID
- `name`: Query name
- `filters`: Filter configuration
- `columns`: Columns to display
- `sortBy`: Sort configuration
- `groupBy`: Group field
- `public`: Visible to others

## Filter Format

```python
[
    {"status": {"operator": "o", "values": None}},  # Open status
    {"assigned_to": {"operator": "=", "values": ["me"]}},  # Assigned to me
    {"priority": {"operator": "=", "values": ["1", "2"]}}  # High priorities
]
```

## Common Filter Operators

| Operator | Description |
|----------|-------------|
| `=` | Equals |
| `!` | Not equals |
| `o` | Open (status) |
| `c` | Closed (status) |
| `~` | Contains |
| `!~` | Not contains |
| `>` | Greater than |
| `<` | Less than |

## Column IDs

Common columns:
- `id`, `subject`, `status`, `priority`
- `assignee`, `author`, `type`
- `dueDate`, `startDate`, `estimatedTime`
- `project`, `parent`, `category`

## Sort By Format

```python
[["dueDate", "asc"], ["priority", "desc"]]
```

## Examples

```python
# Open tasks assigned to me, sorted by due date
create_query(
    name="My Tasks",
    filters=[
        {"status": {"operator": "o", "values": None}},
        {"assigned_to": {"operator": "=", "values": ["me"]}}
    ],
    columns=["id", "subject", "status", "dueDate"],
    sort_by=[("dueDate", "asc")]
)
```
