---
name: m365-shared
description: "Shared patterns for the Microsoft 365 (m365) CLI: authentication, installation, output formatting, and common flags."
allowed-tools:
  - Bash
  - Read
---

# m365-shared — Shared Patterns

## Installation Check

```bash
which m365
```

If not installed, ask user before installing:

```bash
npm i -g @pnp/cli-microsoft365
```

After install, verify:

```bash
m365 version
```

## Authentication

### Quick Check

```bash
m365 status
```

If not logged in, guide user through login:

```bash
m365 login
```

Default: **device code flow** — hiển thị mã code để xác thực qua trình duyệt. Muốn mở trình duyệt đăng nhập trực tiếp, dùng `m365 login --authType browser`.

For other auth methods (certificate, secret, device code), see `references/authentication.md`.

### Verify Connection

```bash
m365 status -o json
```

Response includes: `connectedAs`, `authType`, `appId`, `appTenant`, `cloudType`.

## Output Format

All m365 commands support:

| Flag | Description |
|------|-------------|
| `-o, --output [format]` | `json` (default), `text`, `csv`, `md`, `none` |
| `--query [jmespath]` | JMESPath client-side filter/projection |
| `--verbose` | Verbose logging |
| `--debug` | Debug logging |

### Best Practices

Always use `json` output with `--query` to minimize token usage:

```bash
# BAD: dumps everything
m365 teams team list -o json

# GOOD: only what we need
m365 teams team list -o json --query '[].{id:id, name:displayName}'
```

### JMESPath Patterns

```bash
# Select specific fields
--query '[].{id:id, name:displayName}'

# Filter by condition
--query "[?visibility=='Public'].{id:id, name:displayName}"

# Single item (first match)
--query '[0]'

# Count
--query 'length(@)'

# Nested field
--query '[].{id:id, email:owner.email}'
```

## ID Lookup Workflow

Most m365 commands need IDs (team ID, channel ID, site URL, etc.). General pattern:

1. List resources to find the ID
2. Use the ID in subsequent commands

```bash
# Step 1: Find team ID
m365 teams team list --joined -o json --query "[?contains(displayName,'Project')].{id:id, name:displayName}"

# Step 2: Use team ID to list channels
m365 teams channel list --teamId "TEAM_ID" -o json --query '[].{id:id, name:displayName}'
```

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `You're not logged in` | No active session | Run `m365 login` |
| `Access denied` | Insufficient permissions | Check required permissions in `--help` |
| `Resource not found` | Wrong ID or URL | Verify resource exists via list command |
| `Request throttled` | Too many requests | Wait and retry |

## Security Rules

- NEVER output tokens, secrets, or credentials in responses
- Confirm with user before any destructive operation (remove, delete)
- Prefer `--output none` for write operations when response is not needed
- Use `--query` to exclude sensitive fields from output
