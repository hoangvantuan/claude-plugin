# Work Package Relation Types

## Dependency Relations

| Type | Meaning | Inverse |
|------|---------|---------|
| precedes | Must finish before | follows |
| follows | Must start after | precedes |
| blocks | Blocks progress | blocked |
| blocked | Is blocked by | blocks |

## Structural Relations

| Type | Meaning | Inverse |
|------|---------|---------|
| parent | Has parent (via _links) | children |
| includes | Contains | partof |
| partof | Is part of | includes |

## Logical Relations

| Type | Meaning | Inverse |
|------|---------|---------|
| relates | Generic relation | relates |
| duplicates | Is duplicate of | duplicated |
| duplicated | Has duplicate | duplicates |
| requires | Requires completion of | required |
| required | Is required by | requires |

## Lag Parameter

For `precedes`/`follows` relations, use `delay` (maps to API's `lag`) to set days between WPs:

```python
# Task B follows Task A with 3 day gap
create_relation(from_id=A, to_id=B, relation_type="follows", delay=3)
```

## Usage

```python
# Task B follows Task A (A must finish first)
create_relation(from_id=A, to_id=B, relation_type="follows")

# Bug duplicates Issue
create_relation(from_id=bug_id, to_id=issue_id, relation_type="duplicates")

# Feature blocks Release
create_relation(from_id=feature_id, to_id=release_id, relation_type="blocks")

# With description
create_relation(
    from_id=123,
    to_id=456,
    relation_type="relates",
    description="Related to performance optimization"
)
```

## API Notes

- **Endpoint**: POST `/work_packages/{from_id}/relations`
- Relations are created from `from_id` work package
- `lag` only applicable for `precedes`/`follows` types
