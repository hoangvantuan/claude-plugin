---
name: trello
description: >
  Quản lý Trello workspaces, boards, lists, cards, labels, checklists, members và comments trực tiếp từ Claude.
  Hỗ trợ toàn bộ workflow quản lý task board qua natural language — không cần nhớ API.

  LUÔN dùng skill này khi người dùng đề cập đến Trello, hoặc muốn: chuyển workspace,
  tạo/xem/cập nhật board, tạo/di chuyển/archive card, quản lý list, thêm label/checklist/comment, tìm kiếm card.
  Dùng cả khi người dùng nói "task board", "kanban", "sprint board" mà không đề cập Trello tên.
swagger: https://dac-static.atlassian.com/cloud/trello/swagger.v3.json?_v=1.957.0
---

# Trello Skill

Quản lý Trello qua natural language — Claude dịch yêu cầu thành API call, trả kết quả có cấu trúc.

## Setup

1. Lấy API key: https://trello.com/app-key
2. Tạo Token (click link "Token" trên cùng trang)
3. Set env vars:
   ```bash
   export TRELLO_API_KEY="your-api-key"
   export TRELLO_TOKEN="your-token"
   ```

## Nguyên tắc vận hành

**Auth pattern** — mọi request đều cần:
```
?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN
```

**Base URL**: `https://api.trello.com/1`

**Workflow tìm ID** — Trello dùng ID cho mọi operation. Luôn theo thứ tự:
1. Lấy workspace ID → `GET /members/me/organizations` (nếu cần lọc theo workspace)
2. Lấy board ID → `GET /members/me/boards` hoặc `GET /organizations/{orgId}/boards`
3. Lấy list ID → `GET /boards/{boardId}/lists`
4. Lấy card ID → `GET /lists/{listId}/cards` hoặc `GET /boards/{boardId}/cards`

Sau khi có ID, lưu vào biến shell để dùng lại trong cùng session.

**Xử lý output**: Pipe qua `jq` để format. Dùng `jq '.[].{name,id}'` hoặc custom selectors.

---

## Workspaces (Organizations)

```bash
# Xem tất cả workspaces của tôi
curl -s "https://api.trello.com/1/members/me/organizations?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=displayName,name,id,url" | jq '.[] | {displayName, name, id}'

# Xem chi tiết workspace
curl -s "https://api.trello.com/1/organizations/{orgId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=displayName,name,id,desc,url,memberships" | jq

# Xem boards trong workspace
curl -s "https://api.trello.com/1/organizations/{orgId}/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&filter=open&fields=name,id,url,closed" | jq '.[] | {name, id}'

# Xem members của workspace
curl -s "https://api.trello.com/1/organizations/{orgId}/members?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {fullName, username, id}'

# Tạo workspace mới
curl -s -X POST "https://api.trello.com/1/organizations?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "displayName=Tên Workspace" \
  -d "name=short-name" \
  -d "desc=Mô tả workspace"

# Cập nhật workspace
curl -s -X PUT "https://api.trello.com/1/organizations/{orgId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "displayName=Tên Mới" \
  -d "desc=Mô tả mới"

# Xoá workspace (cảnh báo user — xoá toàn bộ boards bên trong)
curl -s -X DELETE "https://api.trello.com/1/organizations/{orgId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Tạo board trong workspace cụ thể
curl -s -X POST "https://api.trello.com/1/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Tên Board" \
  -d "idOrganization={orgId}" \
  -d "defaultLists=false"
```

Khi user có nhiều workspace, luôn hỏi hoặc list workspaces trước để xác định đúng context.

---

## Boards

```bash
# Xem tất cả boards của tôi
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id,url,closed" | jq '.[] | select(.closed == false) | {name, id}'

# Xem chi tiết một board
curl -s "https://api.trello.com/1/boards/{boardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&lists=open&members=all&labels=all" | jq '{name, id, lists: .lists[].name}'

# Tạo board mới
curl -s -X POST "https://api.trello.com/1/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Tên Board" \
  -d "defaultLists=false"

# Đổi tên board
curl -s -X PUT "https://api.trello.com/1/boards/{boardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Tên Mới"

# Archive board (đóng, không xoá)
curl -s -X PUT "https://api.trello.com/1/boards/{boardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "closed=true"
```

---

## Lists (Columns)

```bash
# Xem tất cả lists trong board
curl -s "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&filter=open" | jq '.[] | {name, id}'

# Tạo list mới
curl -s -X POST "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Tên List" \
  -d "pos=bottom"

# Đổi tên list
curl -s -X PUT "https://api.trello.com/1/lists/{listId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Tên Mới"

# Archive list
curl -s -X PUT "https://api.trello.com/1/lists/{listId}/closed?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "value=true"

# Xem tất cả cards trong list
curl -s "https://api.trello.com/1/lists/{listId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id,desc,due,labels" | jq
```

---

## Cards

```bash
# Xem cards trong board (có thể filter theo list name)
curl -s "https://api.trello.com/1/boards/{boardId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id,idList,desc,due,labels,checklists" | jq

# Xem chi tiết card
curl -s "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&checklists=all&members=true&attachments=true" | jq

# Tạo card mới
curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={listId}" \
  -d "name=Tên Card" \
  -d "desc=Mô tả chi tiết" \
  -d "pos=bottom"

# Cập nhật card (đổi tên, mô tả, due date)
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Tên Mới" \
  -d "desc=Mô tả mới" \
  -d "due=2025-12-31T23:59:59.000Z"

# Di chuyển card sang list khác
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={newListId}"

# Di chuyển card sang board khác
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idBoard={newBoardId}" \
  -d "idList={newListId}"

# Archive card
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "closed=true"

# Xoá card (vĩnh viễn — cảnh báo user trước)
curl -s -X DELETE "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Mark due date complete
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "dueComplete=true"
```

---

## Labels

```bash
# Xem labels của board
curl -s "https://api.trello.com/1/boards/{boardId}/labels?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, color}'

# Tạo label mới
# Màu hợp lệ: black, blue, green, lime, orange, pink, purple, red, sky, yellow, null (không màu)
curl -s -X POST "https://api.trello.com/1/labels?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Bug" \
  -d "color=red" \
  -d "idBoard={boardId}"

# Gán label vào card
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/idLabels?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "value={labelId}"

# Gỡ label khỏi card
curl -s -X DELETE "https://api.trello.com/1/cards/{cardId}/idLabels/{labelId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Cập nhật label
curl -s -X PUT "https://api.trello.com/1/labels/{labelId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Tên Mới" \
  -d "color=blue"
```

---

## Checklists

```bash
# Xem checklists của card
curl -s "https://api.trello.com/1/cards/{cardId}/checklists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, checkItems}'

# Tạo checklist mới trong card
curl -s -X POST "https://api.trello.com/1/checklists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idCard={cardId}" \
  -d "name=Tên Checklist"

# Thêm item vào checklist
curl -s -X POST "https://api.trello.com/1/checklists/{checklistId}/checkItems?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Tên task item" \
  -d "checked=false" \
  -d "pos=bottom"

# Đánh dấu item hoàn thành / chưa xong
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}/checkItem/{checkItemId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "state=complete"    # hoặc "incomplete"

# Xoá checklist item
curl -s -X DELETE "https://api.trello.com/1/checklists/{checklistId}/checkItems/{checkItemId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Xoá toàn bộ checklist
curl -s -X DELETE "https://api.trello.com/1/checklists/{checklistId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```

---

## Comments

```bash
# Xem comments của card (qua actions)
curl -s "https://api.trello.com/1/cards/{cardId}/actions?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&filter=commentCard" | jq '.[] | {date, text: .data.text, by: .memberCreator.fullName}'

# Thêm comment
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/actions/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "text=Nội dung comment"

# Xoá comment (cần actionId từ bước xem comments)
curl -s -X DELETE "https://api.trello.com/1/actions/{actionId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```

---

## Members

```bash
# Xem thông tin bản thân
curl -s "https://api.trello.com/1/members/me?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=fullName,username,id" | jq

# Xem members của board
curl -s "https://api.trello.com/1/boards/{boardId}/members?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {fullName, username, id}'

# Assign member vào card
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/idMembers?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "value={memberId}"

# Bỏ assign member khỏi card
curl -s -X DELETE "https://api.trello.com/1/cards/{cardId}/idMembers/{memberId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Xem cards được assign cho một member
curl -s "https://api.trello.com/1/members/{memberId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id,idBoard,idList" | jq
```

---

## Tìm kiếm (Search)

```bash
# Tìm card/board theo từ khoá
curl -s "https://api.trello.com/1/search?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&query=keyword&modelTypes=cards,boards&cards_fields=name,id,idList,idBoard" | jq

# Tìm card trong board cụ thể
curl -s "https://api.trello.com/1/search?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&query=keyword&idBoards={boardId}&modelTypes=cards" | jq '.cards[] | {name, id}'

# Tìm card theo member
curl -s "https://api.trello.com/1/search?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&query=@{username}&modelTypes=cards" | jq '.cards[] | {name, id}'
```

---

## Workflow phức tạp hay dùng

### Lấy snapshot toàn bộ board (1 lần call)
```bash
curl -s "https://api.trello.com/1/boards/{boardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&lists=open&cards=open&card_fields=name,idList,desc,due,labels,dueComplete&labels=all&members=all&fields=name,id" | jq
```

### Di chuyển toàn bộ cards từ list này sang list kia
```bash
curl -s -X POST "https://api.trello.com/1/lists/{sourceListId}/moveAllCards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idBoard={boardId}" \
  -d "idList={targetListId}"
```

### Lấy activity log của board (N actions gần nhất)
```bash
curl -s "https://api.trello.com/1/boards/{boardId}/actions?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&limit=50" | jq '.[] | {type, date, memberCreator: .memberCreator.fullName}'
```

### Batch request (tối đa 10 calls trong 1 request)
```bash
curl -s "https://api.trello.com/1/batch?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&urls=/members/me/boards,/members/me/cards" | jq
```

---

## Giới hạn & lưu ý

- **Rate limit**: 300 requests/10s (per API key); 100 requests/10s (per token)
- **Endpoint `/1/members`**: giới hạn 100 requests/900s — tránh call liên tục
- **Delete card**: vĩnh viễn, không undo được — hỏi confirm user trước khi xoá
- **Delete board**: không có API delete board trực tiếp — chỉ archive (closed=true)
- **IDs**: stable, không đổi kể cả khi rename board/list/card
- **Date format**: ISO 8601 — ví dụ `2025-12-31T23:59:59.000Z`
- **Position**: dùng `"top"`, `"bottom"`, hoặc số float để sắp thứ tự chính xác

Chi tiết đầy đủ endpoint: xem [references/api-reference.md](references/api-reference.md)
