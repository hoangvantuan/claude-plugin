# Trello API Quick Reference

Base URL: `https://api.trello.com/1`
Auth: `?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN` (append vào mọi request)

## Workspaces (Organizations)

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/members/me/organizations` | Tất cả workspaces của tôi |
| GET | `/organizations/{id}` | Chi tiết workspace |
| GET | `/organizations/{id}/boards` | Boards trong workspace (`?filter=open/closed/all`) |
| GET | `/organizations/{id}/members` | Members của workspace |
| GET | `/organizations/{id}/memberships` | Membership details (role, type) |
| POST | `/organizations` | Tạo workspace (`displayName`, `name`, `desc`) |
| PUT | `/organizations/{id}` | Cập nhật (`displayName`, `name`, `desc`, `website`) |
| DELETE | `/organizations/{id}` | Xoá workspace (vĩnh viễn — xoá cả boards bên trong) |

**Lưu ý**: `name` là short name (dùng trong URL), `displayName` là tên hiển thị đầy đủ.

## Boards

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/members/me/boards` | Tất cả boards của tôi |
| GET | `/boards/{id}` | Chi tiết board |
| GET | `/boards/{id}/lists` | Lists trong board (`?filter=open/closed/all`) |
| GET | `/boards/{id}/cards` | Tất cả cards trong board |
| GET | `/boards/{id}/members` | Members của board |
| GET | `/boards/{id}/labels` | Labels của board |
| GET | `/boards/{id}/actions` | Activity log (`?limit=50`) |
| POST | `/boards` | Tạo board (`name`, `defaultLists`) |
| PUT | `/boards/{id}` | Cập nhật board (`name`, `desc`, `closed`) |

## Lists

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/lists/{id}` | Chi tiết list |
| GET | `/lists/{id}/cards` | Cards trong list |
| POST | `/boards/{id}/lists` | Tạo list (`name`, `pos`) |
| PUT | `/lists/{id}` | Cập nhật list (`name`, `pos`) |
| PUT | `/lists/{id}/closed` | Archive list (`value=true/false`) |
| POST | `/lists/{id}/moveAllCards` | Move tất cả cards (`idBoard`, `idList`) |

## Cards

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/cards/{id}` | Chi tiết card |
| GET | `/cards/{id}/actions` | Activity của card (`?filter=commentCard`) |
| GET | `/cards/{id}/checklists` | Checklists của card |
| GET | `/cards/{id}/attachments` | Attachments của card |
| POST | `/cards` | Tạo card (`idList`, `name`, `desc`, `due`, `pos`) |
| PUT | `/cards/{id}` | Cập nhật (`name`, `desc`, `idList`, `idBoard`, `due`, `dueComplete`, `closed`) |
| DELETE | `/cards/{id}` | Xoá vĩnh viễn card |
| POST | `/cards/{id}/actions/comments` | Thêm comment (`text`) |
| POST | `/cards/{id}/idLabels` | Gán label (`value={labelId}`) |
| DELETE | `/cards/{id}/idLabels/{labelId}` | Gỡ label |
| POST | `/cards/{id}/idMembers` | Assign member (`value={memberId}`) |
| DELETE | `/cards/{id}/idMembers/{memberId}` | Bỏ assign |
| PUT | `/cards/{id}/checkItem/{checkItemId}` | Update checklist item (`state=complete/incomplete`) |
| POST | `/cards/{id}/attachments` | Thêm attachment (`url` hoặc `file`) |

## Labels

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/labels/{id}` | Chi tiết label |
| POST | `/labels` | Tạo label (`name`, `color`, `idBoard`) |
| PUT | `/labels/{id}` | Cập nhật (`name`, `color`) |
| DELETE | `/labels/{id}` | Xoá label |

**Màu hợp lệ**: `black`, `blue`, `green`, `lime`, `orange`, `pink`, `purple`, `red`, `sky`, `yellow`, `null`

## Checklists

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/checklists/{id}` | Chi tiết checklist |
| POST | `/checklists` | Tạo checklist (`idCard`, `name`) |
| DELETE | `/checklists/{id}` | Xoá checklist |
| POST | `/checklists/{id}/checkItems` | Thêm item (`name`, `pos`, `checked`) |
| GET | `/checklists/{id}/checkItems/{checkItemId}` | Chi tiết item |
| PUT | `/checklists/{id}/checkItems/{checkItemId}` | Cập nhật item (`name`, `state`, `pos`) |
| DELETE | `/checklists/{id}/checkItems/{checkItemId}` | Xoá item |

## Members

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/members/me` | Thông tin bản thân |
| GET | `/members/{id}` | Thông tin member |
| GET | `/members/{id}/boards` | Boards của member |
| GET | `/members/{id}/cards` | Cards được assign |

## Actions (Comments, History)

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/actions/{id}` | Chi tiết action |
| PUT | `/actions/{id}` | Sửa comment (`text`) |
| DELETE | `/actions/{id}` | Xoá action/comment |

## Search

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/search` | Tìm kiếm (`query`, `modelTypes=cards,boards,members`, `idBoards`, `cards_limit`) |

## Batch

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/batch` | Tối đa 10 URLs trong 1 request (`urls=/path1,/path2`) |

---

## Query Parameters hay dùng

| Parameter | Áp dụng cho | Giá trị |
|-----------|------------|---------|
| `fields` | GET | `all` hoặc comma-separated: `name,id,desc,due` |
| `filter` | boards, lists, cards | `open`, `closed`, `all` |
| `members` | boards, cards | `true/false` hoặc `all` |
| `checklists` | cards | `all`, `none` |
| `attachments` | cards | `true/false` |
| `labels` | boards | `all` |
| `limit` | actions | Số nguyên (max 1000) |

---

## jq Patterns hay dùng

```bash
# Lấy name + id từ array
jq '.[] | {name, id}'

# Filter theo tên (case-insensitive)
jq '.[] | select(.name | ascii_downcase | contains("sprint"))'

# Lấy cards chưa xong (chưa archive)
jq '[.[] | select(.closed == false)]'

# Đếm số cards theo list
jq 'group_by(.idList) | map({list: .[0].idList, count: length})'

# Lấy text comments
jq '.[] | {date, comment: .data.text, by: .memberCreator.fullName}'
```
