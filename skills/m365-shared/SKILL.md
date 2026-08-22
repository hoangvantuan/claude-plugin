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

Default: **device code flow** — prints a code you enter in a browser to authenticate. To open a browser and sign in directly, use `m365 login --authType browser`.

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
| `Request failed with status code 4xx` | `m365 request` swallows the Graph error body | Rerun the same call with `--debug`, see below |

### Reading the real error behind a failed `m365 request`

On a 4xx, `m365 request` prints only the status line and drops the response body, which is where Graph states what is actually wrong. Rerun the identical call with `--debug` and read the `Request error:` block:

```bash
# Without --debug:  Error: Request failed with status code 400
m365 request --url 'https://graph.microsoft.com/v1.0/me/events?$select=nonExistent' -o json --debug 2>&1 \
  | grep -E '"code"|"message"'
# "code": "RequestBroker--ParseUri",
# "message": "Could not find a property named 'nonExistent' on type 'Microsoft.OutlookServices.Event'."
```

Do this before guessing at a cause: a 400 from a malformed request body and a 400 from a wrong property name look identical without it.

## Security Rules

- NEVER output tokens, secrets, or credentials in responses
- Confirm with user before any destructive operation (remove, delete)
- Prefer `--output none` for write operations when response is not needed
- Use `--query` to exclude sensitive fields from output
