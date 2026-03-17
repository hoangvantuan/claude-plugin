---
name: things-manager
description: Manage Things 3 tasks, projects, areas, and tags via things-cli (Go CLI). Use whenever the user mentions Things 3, task management, todo lists, creating/completing/editing tasks, listing projects or areas, or any personal productivity workflow involving Things. Also trigger when user says "add task", "complete task", "show my tasks", "what's on my plate today", or references Things app in any way.
allowed-tools:
  - Bash
  - Read
---

# Things 3 Manager

Manage Things 3 cloud tasks via `things-cli` — a Go CLI that syncs with Things Cloud.

## Prerequisites

### 1. Install Go (if not installed)

```bash
brew install go
```

### 2. Install things-cli

The official `go install` is broken due to module path mismatch. Install from source:

```bash
git clone --depth 1 https://github.com/arthursoares/things-cloud-sdk.git /tmp/things-cloud-sdk
cd /tmp/things-cloud-sdk && go install ./cmd/things-cli/
```

Binary installs to `~/go/bin/things-cli`.

### 3. Environment Variables

Required in shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export THINGS_USERNAME="your-things-cloud-email"
export THINGS_PASSWORD="your-things-cloud-password"
export PATH="$HOME/go/bin:$PATH"
```

Optional: `export THINGS_DEBUG=1` for debug output.

## CLI Reference

Binary: `~/go/bin/things-cli`

Always set PATH before running:
```bash
export PATH="$HOME/go/bin:/opt/homebrew/bin:$PATH"
```

### Read Commands

These load state from Things Cloud first.

```bash
# List tasks (default: all non-completed)
things-cli list
things-cli list --today        # Today view
things-cli list --inbox        # Inbox only
things-cli list --area "Work"  # Filter by area name
things-cli list --project "My Project"  # Filter by project name

# Show single task details
things-cli show <uuid>

# List all areas
things-cli areas

# List all projects
things-cli projects

# List all tags
things-cli tags
```

### Write Commands

These are fast — they skip state loading and send operations directly.

```bash
# Create task
things-cli create "Task title" \
  --note "Description here" \
  --when today|anytime|someday|inbox \
  --deadline 2026-03-20 \
  --scheduled 2026-03-18 \
  --project <uuid> \
  --heading <uuid> \
  --area <uuid> \
  --tags <uuid1>,<uuid2> \
  --type task|project|heading \
  --checklist "Item 1,Item 2,Item 3"

# Create area
things-cli create-area "Area Name" --tags <uuid,...> --uuid <custom-uuid>

# Create tag
things-cli create-tag "Tag Name" --shorthand KEY --parent <uuid>

# Add checklist items to existing task
things-cli add-checklist <task-uuid> "Item 1,Item 2,Item 3"

# Edit task
things-cli edit <uuid> \
  --title "New title" \
  --note "Updated note" \
  --when today \
  --deadline 2026-04-01 \
  --scheduled 2026-03-25 \
  --area <uuid> \
  --project <uuid> \
  --heading <uuid> \
  --tags <uuid1>,<uuid2>

# Complete task
things-cli complete <uuid>

# Trash task (move to trash)
things-cli trash <uuid>

# Purge task (permanently delete)
things-cli purge <uuid>

# Move task to Today
things-cli move-to-today <uuid>
```

### Batch Operations

Send multiple operations in one HTTP request via JSON stdin:

```bash
echo '[
  {"cmd": "create", "title": "Task 1", "when": "today"},
  {"cmd": "create", "title": "Task 2", "project": "uuid-here"},
  {"cmd": "complete", "uuid": "abc-123"},
  {"cmd": "trash", "uuid": "def-456"},
  {"cmd": "move-to-today", "uuid": "ghi-789"},
  {"cmd": "move-to-project", "uuid": "xxx", "project": "yyy"},
  {"cmd": "move-to-area", "uuid": "xxx", "area": "yyy"},
  {"cmd": "edit", "uuid": "xxx", "title": "New title", "note": "Updated"}
]' | things-cli batch
```

Batch is useful when creating multiple tasks at once or performing bulk operations — it's significantly faster than individual commands because it combines everything into a single API call.

## Usage Patterns

### Workflow: List then act

For operations that need a UUID (edit, complete, trash), first list to find the task:

```bash
things-cli list --today    # Find the UUID
things-cli complete <uuid> # Then act on it
```

### Workflow: Quick capture

For fast task creation, no need to list first:

```bash
things-cli create "Buy groceries" --when today
things-cli create "Review PR #42" --when today --note "Focus on auth changes"
```

### Workflow: Bulk create from plan

When creating multiple related tasks:

```bash
echo '[
  {"cmd": "create", "title": "Design API schema", "when": "today"},
  {"cmd": "create", "title": "Implement endpoints", "when": "anytime"},
  {"cmd": "create", "title": "Write tests", "when": "anytime"}
]' | things-cli batch
```

## Error Handling

- If `things-cli` is not found: check `~/go/bin/` exists and PATH is set
- If "THINGS_USERNAME is required": env vars not set — check `~/.zshrc`
- If connection errors: verify Things Cloud credentials are correct
- If UUID not found: the task may have been completed or trashed already

## Output Format

When presenting task lists to the user, format as a clean readable list showing title, status, and relevant dates. For single task details, show all available fields.
