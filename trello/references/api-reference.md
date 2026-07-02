# Trello API Quick Reference

Base URL: `https://api.trello.com/1`
Auth: `?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN` (append to every request)

## Workspaces (Organizations)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/members/me/organizations` | All my workspaces |
| GET | `/organizations/{id}` | Workspace details |
| GET | `/organizations/{id}/boards` | Boards in workspace (`?filter=open/closed/all`) |
| GET | `/organizations/{id}/members` | Workspace members |
| GET | `/organizations/{id}/memberships` | Membership details (role, type) |
| POST | `/organizations` | Create workspace (`displayName`, `name`, `desc`) |
| PUT | `/organizations/{id}` | Update (`displayName`, `name`, `desc`, `website`) |
| DELETE | `/organizations/{id}` | Delete workspace (permanent — deletes all boards inside) |

**Note**: `name` is the short name (used in URL), `displayName` is the full display name.

## Boards

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/members/me/boards` | All my boards |
| GET | `/boards/{id}` | Board details |
| GET | `/boards/{id}/lists` | Lists in board (`?filter=open/closed/all`) |
| GET | `/boards/{id}/cards` | All cards in board |
| GET | `/boards/{id}/members` | Board members |
| GET | `/boards/{id}/checklists` | All checklists in board (progress overview) |
| GET | `/boards/{id}/labels` | Board labels |
| GET | `/boards/{id}/actions` | Activity log (`?limit=50`) |
| POST | `/boards` | Create board (`name`, `defaultLists`, `idOrganization`) |
| PUT | `/boards/{id}` | Update board (`name`, `desc`, `closed`) |
| DELETE | `/boards/{id}` | Delete board permanently (prefer archive `closed=true`) |
| PUT | `/boards/{id}/members` | Invite member to board via email |
| PUT | `/boards/{id}/members/{idMember}` | Add member to board (`type`: admin/normal/observer) |
| DELETE | `/boards/{id}/members/{idMember}` | Remove member from board |
| GET | `/boards/{id}/boardPlugins` | Active Power-Ups on board |
| GET | `/boards/{id}/plugins` | All Power-Ups on board |

## Lists

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/lists/{id}` | List details |
| GET | `/lists/{id}/cards` | Cards in list |
| POST | `/boards/{id}/lists` | Create list (`name`, `pos`) |
| PUT | `/lists/{id}` | Update list (`name`, `pos`) |
| PUT | `/lists/{id}/closed` | Archive list (`value=true/false`) |
| POST | `/lists/{id}/archiveAllCards` | Archive all cards in list |
| PUT | `/lists/{id}/idBoard` | Move list to another board (`value={boardId}`) |
| POST | `/lists/{id}/moveAllCards` | Move all cards (`idBoard`, `idList`) |

## Cards

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cards/{id}` | Card details |
| GET | `/cards/{id}/actions` | Card activity (`?filter=commentCard`) |
| GET | `/cards/{id}/checklists` | Card checklists |
| GET | `/cards/{id}/attachments` | Card attachments |
| POST | `/cards` | Create card (`idList`, `name`, `desc`, `due`, `pos`) |
| PUT | `/cards/{id}` | Update (`name`, `desc`, `idList`, `idBoard`, `due`, `dueComplete`, `closed`) |
| DELETE | `/cards/{id}` | Delete card permanently |
| POST | `/cards/{id}/actions/comments` | Add comment (`text`) |
| POST | `/cards/{id}/idLabels` | Assign label (`value={labelId}`) |
| DELETE | `/cards/{id}/idLabels/{labelId}` | Remove label |
| POST | `/cards/{id}/idMembers` | Assign member (`value={memberId}`) |
| DELETE | `/cards/{id}/idMembers/{memberId}` | Unassign member |
| PUT | `/cards/{id}/checkItem/{checkItemId}` | Update checklist item (`state=complete/incomplete`) |
| POST | `/cards/{id}/attachments` | Add attachment (`url` or `file`) |
| GET | `/cards/{id}/attachments/{idAttachment}` | Attachment details |
| DELETE | `/cards/{id}/attachments/{idAttachment}` | Delete attachment |
| PUT | `/cards/{id}/actions/{idAction}/comments` | Edit comment (`text`) |
| DELETE | `/cards/{id}/actions/{idAction}/comments` | Delete comment (card-scoped) |
| GET | `/cards/{id}/pluginData` | Power-Up data on card |

## Labels

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/labels/{id}` | Label details |
| POST | `/labels` | Create label (`name`, `color`, `idBoard`) |
| PUT | `/labels/{id}` | Update (`name`, `color`) |
| DELETE | `/labels/{id}` | Delete label |

**Valid colors**: `black`, `blue`, `green`, `lime`, `orange`, `pink`, `purple`, `red`, `sky`, `yellow`, `null`

## Checklists

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/checklists/{id}` | Checklist details |
| POST | `/checklists` | Create checklist (`idCard`, `name`) |
| DELETE | `/checklists/{id}` | Delete checklist |
| POST | `/checklists/{id}/checkItems` | Add item (`name`, `pos`, `checked`) |
| GET | `/checklists/{id}/checkItems/{checkItemId}` | Item details |
| PUT | `/checklists/{id}/checkItems/{checkItemId}` | Update item (`name`, `state`, `pos`) |
| DELETE | `/checklists/{id}/checkItems/{checkItemId}` | Delete item |

## Members

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/members/me` | My info |
| GET | `/members/{id}` | Member info |
| GET | `/members/{id}/boards` | Member's boards |
| GET | `/members/{id}/cards` | Assigned cards |

## Actions (Comments, History)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/actions/{id}` | Action details |
| PUT | `/actions/{id}` | Edit comment (`text`) |
| DELETE | `/actions/{id}` | Delete action/comment |

## Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/search` | Search (`query`, `modelTypes=cards,boards,members`, `idBoards`, `idOrganizations`, `cards_limit`) |

## Batch

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/batch` | Up to 10 URLs in 1 request (`urls=/path1,/path2`) |

---

## Common Query Parameters

| Parameter | Applies to | Values |
|-----------|-----------|--------|
| `fields` | GET | `all` or comma-separated: `name,id,desc,due` |
| `filter` | boards, lists, cards | `open`, `closed`, `all` |
| `members` | boards, cards | `true/false` or `all` |
| `checklists` | cards | `all`, `none` |
| `attachments` | cards | `true/false` |
| `labels` | boards | `all` |
| `limit` | actions | Integer (max 1000) |

---

## Common jq Patterns

```bash
# Get name + id from array
jq '.[] | {name, id}'

# Filter by name (case-insensitive)
jq '.[] | select(.name | ascii_downcase | contains("sprint"))'

# Get non-archived cards
jq '[.[] | select(.closed == false)]'

# Count cards per list
jq 'group_by(.idList) | map({list: .[0].idList, count: length})'

# Get comment text
jq '.[] | {date, comment: .data.text, by: .memberCreator.fullName}'
```
