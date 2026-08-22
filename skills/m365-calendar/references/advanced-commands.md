# Advanced commands — calendargroup, chia sẻ calendar, đường admin

Những thứ ở đây ít dùng hơn hẳn phần trong SKILL.md. Đọc khi gặp đúng nhu cầu.

## 1. Calendar group

Nhóm calendar là cách Outlook gom nhiều calendar lại cho gọn ("Lịch của tôi", "Lịch nhóm"). Nhóm `My Calendars` là nhóm mặc định, luôn có sẵn.

Lệnh native có `get`, `list`, `set`, `remove` nhưng **không có `add`**, tức tạo nhóm mới phải đi qua Graph.

```bash
USER=$(m365 status -o json --query 'connectedAs' | tr -d '"')

# Liệt kê nhóm
m365 outlook calendargroup list --userName "$USER" -o json --query '[].{id:id, name:name, classId:classId}'

# Lấy một nhóm
m365 outlook calendargroup get --userName "$USER" --name "My Calendars" -o json

# Đổi tên nhóm
m365 outlook calendargroup set --userName "$USER" --id "GROUP_ID" --name "Tên mới"

# Xoá nhóm (calendar bên trong bị xoá theo, hỏi người dùng trước)
m365 outlook calendargroup remove --userName "$USER" --name "Tên nhóm" --force

# Tạo nhóm mới (không có lệnh native, đi qua Graph)
m365 request --url 'https://graph.microsoft.com/v1.0/me/calendarGroups' --method post \
  --content-type "application/json" --body '{"name":"Lịch dự án"}' -o json --query '{id:id, name:name}'
```

Tạo calendar trực tiếp vào một nhóm thì `outlook calendar add` có sẵn `--calendarGroupName`:

```bash
m365 outlook calendar add --userName "$USER" --name "Dự án Alpha" --calendarGroupName "Lịch dự án" -o json --query 'id'
```

## 2. Chia sẻ calendar cho người khác

Không có lệnh native, đi qua Graph `calendarPermissions`.

```bash
# Xem ai đang được chia sẻ
m365 request --url 'https://graph.microsoft.com/v1.0/me/calendar/calendarPermissions' -o json \
  --query 'value[].{who:emailAddress.name, role:role, id:id}'

# Chia sẻ cho một người
SP="${TMPDIR:-/tmp}"
cat > "$SP/perm.json" <<'JSON'
{
  "emailAddress": { "name": "Người A", "address": "nguoia@contoso.com" },
  "role": "read",
  "allowedRoles": ["read"]
}
JSON
m365 request --url 'https://graph.microsoft.com/v1.0/me/calendar/calendarPermissions' --method post \
  --content-type "application/json" --body "@$SP/perm.json" -o json --query '{id:id, role:role}'

# Thu hồi quyền
m365 request --url 'https://graph.microsoft.com/v1.0/me/calendar/calendarPermissions/PERMISSION_ID' --method delete -o none
```

Các mức `role`: `freeBusyRead` (chỉ thấy rảnh bận), `limitedRead` (thấy tiêu đề), `read`, `write`, `delegateWithoutPrivateEventAccess`, `delegateWithPrivateEventAccess`, `custom`.

Chia sẻ calendar là thay đổi ai được xem dữ liệu của mình, nên xác nhận rõ với người dùng địa chỉ nhận và mức quyền trước khi chạy.

## 3. Đường phòng họp mức admin

Nếu Exchange admin đã cấp `Place.Read.All`, hai đường này hoạt động và ổn định hơn `beta/me/findRooms`:

```bash
# Lệnh native
m365 outlook room list -o json --query '[].{name:displayName, email:emailAddress}'
m365 outlook room list --roomlistEmail "toanha2@contoso.com" -o json
m365 outlook roomlist list -o json --query '[].{name:displayName, email:emailAddress}'

# Graph v1.0
m365 request --url 'https://graph.microsoft.com/v1.0/places/microsoft.graph.room' -o json \
  --query 'value[].{name:displayName, email:emailAddress, capacity:capacity, floor:floorLabel}'
```

Không có quyền thì cả ba trả 403, khi đó dùng `beta/me/findRooms` trong `graph-recipes.md`. Ưu điểm của đường admin: có thêm `capacity` (số chỗ) và `floorLabel` (tầng), thứ mà `findRooms` không trả về.

## 4. Những thứ không khả dụng với app mặc định của m365 CLI

| Nhu cầu | Endpoint | Trạng thái |
|---------|----------|------------|
| giờ làm việc, múi giờ ưa dùng | `me/mailboxSettings` | 403, thiếu `MailboxSettings.Read` |
| trả lời tự động (auto reply) | `me/mailboxSettings/automaticRepliesSetting` | 403, cùng lý do |
| danh sách phòng qua `/places` | `v1.0/places/...` | 403, thiếu `Place.Read.All` |

Muốn mở các scope này thì phải đăng nhập bằng Microsoft Entra app riêng (`m365 login --appId ...`) thay cho app mặc định. Việc đó đổi cách xác thực của **cả bốn** skill m365, nên nếu cần thì làm ở `../m365-shared/references/authentication.md` chứ không phải ở đây.
