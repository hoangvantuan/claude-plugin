---
name: trello
description: >
  Manage Trello workspaces, boards, lists, cards, labels, checklists, members and comments directly from Claude.
  Supports the full task board management workflow via natural language — no need to remember the API.

  ALWAYS use this skill when the user mentions Trello, or wants to: switch workspaces,
  create/view/update boards, create/move/archive cards, manage lists, add labels/checklists/comments, search cards.
  Also use when the user says "task board", "kanban", "sprint board" without explicitly mentioning Trello.
swagger: https://dac-static.atlassian.com/cloud/trello/swagger.v3.json?_v=1.957.0
---

# Trello Skill

Manage Trello via natural language — Claude translates requests into API calls and returns structured results.

## Setup

1. Get API key: https://trello.com/app-key
2. Create Token (click the "Token" link on that same page)
3. Set env vars:
   ```bash
   export TRELLO_API_KEY="your-api-key"
   export TRELLO_TOKEN="your-token"
   ```

## Operating Principles

**Auth pattern** — every request requires:
```
?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN
```

**Base URL**: `https://api.trello.com/1`

**ID lookup workflow** — Trello uses IDs for all operations. Always follow this order:
1. Get workspace ID → `GET /members/me/organizations` (if filtering by workspace)
2. Get board ID → `GET /members/me/boards` or `GET /organizations/{orgId}/boards`
3. Get list ID → `GET /boards/{boardId}/lists`
4. Get card ID → `GET /lists/{listId}/cards` or `GET /boards/{boardId}/cards`

After obtaining IDs, store them in shell variables for reuse within the same session.

**Output handling**: Pipe through `jq` for formatting. Use `jq '.[] | {name, id}'` or custom selectors.

---

## Determining Context — Workspaces & Boards

```bash
# View all workspaces
curl -s "https://api.trello.com/1/members/me/organizations?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=displayName,name,id,url" | jq '.[] | {displayName, name, id}'

# View boards in a workspace
curl -s "https://api.trello.com/1/organizations/{orgId}/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&filter=open&fields=name,id,url,closed" | jq '.[] | {name, id}'

# View all my boards (not filtered by workspace)
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id,url,closed" | jq '.[] | select(.closed == false) | {name, id}'

# View board details
curl -s "https://api.trello.com/1/boards/{boardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&lists=open&members=all&labels=all" | jq '{name, id, lists: [.lists[].name]}'

# Create a new board
curl -s -X POST "https://api.trello.com/1/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Board Name" \
  -d "defaultLists=false"

# Rename a board
curl -s -X PUT "https://api.trello.com/1/boards/{boardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=New Name"

# Archive board (close, not delete)
curl -s -X PUT "https://api.trello.com/1/boards/{boardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "closed=true"

# Delete board (permanent — warn user first, prefer archive)
curl -s -X DELETE "https://api.trello.com/1/boards/{boardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```

When the user has multiple workspaces, always list workspaces first to determine the correct context.
Full workspace CRUD: see [references/workspaces.md](references/workspaces.md)

---

## Lists (Columns)

```bash
# View all lists in a board
curl -s "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&filter=open" | jq '.[] | {name, id}'

# Create a new list
curl -s -X POST "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=List Name" \
  -d "pos=bottom"

# Rename a list
curl -s -X PUT "https://api.trello.com/1/lists/{listId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=New Name"

# Archive a list
curl -s -X PUT "https://api.trello.com/1/lists/{listId}/closed?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "value=true"

# View all cards in a list
curl -s "https://api.trello.com/1/lists/{listId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id,desc,due,labels" | jq

# Archive all cards in a list (cards remain, just hidden)
curl -s -X POST "https://api.trello.com/1/lists/{listId}/archiveAllCards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Move a list to another board
curl -s -X PUT "https://api.trello.com/1/lists/{listId}/idBoard?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "value={newBoardId}"
```

---

## Cards

```bash
# View cards in a board
curl -s "https://api.trello.com/1/boards/{boardId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id,idList,desc,due,labels,checklists" | jq

# View card details
curl -s "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&checklists=all&members=true&attachments=true" | jq

# Create a new card
curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={listId}" \
  -d "name=Card Name" \
  -d "desc=Detailed description" \
  -d "pos=bottom"

# Update a card (rename, description, due date)
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=New Name" \
  -d "desc=New description" \
  -d "due=2025-12-31T23:59:59.000Z"

# Move card to another list
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={newListId}"

# Move card to another board
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idBoard={newBoardId}" \
  -d "idList={newListId}"

# Archive a card
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "closed=true"

# Delete a card (permanent — warn user first)
curl -s -X DELETE "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Mark due date complete
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "dueComplete=true"

# Set card cover (color or attachment)
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{"cover": {"color": "blue", "size": "normal", "brightness": "dark"}}'
# Or use an attachment as cover:
# {"cover": {"idAttachment": "{attachmentId}", "size": "normal", "brightness": "light"}}
```

---

## Search

```bash
# Search cards/boards by keyword
curl -s "https://api.trello.com/1/search?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&query=keyword&modelTypes=cards,boards&cards_fields=name,id,idList,idBoard" | jq

# Search cards in a specific board
curl -s "https://api.trello.com/1/search?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&query=keyword&idBoards={boardId}&modelTypes=cards" | jq '.cards[] | {name, id}'

# Search cards by member
curl -s "https://api.trello.com/1/search?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&query=@{username}&modelTypes=cards" | jq '.cards[] | {name, id}'
```

---

## Limits & Notes

- **Rate limit**: 300 requests/10s (per API key); 100 requests/10s (per token)
- **Endpoint `/1/members`**: limited to 100 requests/900s — avoid repeated calls
- **Delete card**: permanent, cannot be undone — confirm with user before deleting
- **Delete board**: `DELETE /boards/{id}` — permanent, deletes all lists/cards inside. Prefer archive (`closed=true`) first, only delete when user explicitly confirms
- **Delete workspace**: permanent, deletes all boards inside — confirm with user first
- **IDs**: stable, do not change even when renaming board/list/card
- **Date format**: ISO 8601 — e.g. `2025-12-31T23:59:59.000Z`
- **Position**: use `"top"`, `"bottom"`, or a float number for precise ordering

---

## References — read when needed

| File | When to read |
|------|-------------|
| [workspaces.md](references/workspaces.md) | Create, update, delete workspace; view workspace members |
| [collaboration.md](references/collaboration.md) | Members (assign, invite, remove from board), Comments (CRUD), Attachments (attach file/URL) |
| [task-organization.md](references/task-organization.md) | Labels (create, assign, change color), Checklists (create, check items, delete) |
| [advanced-workflows.md](references/advanced-workflows.md) | Board snapshot, moveAllCards, activity log, pluginData, Power-Ups, batch request |
| [api-reference.md](references/api-reference.md) | Quick lookup table for all endpoints |
