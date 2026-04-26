# API Quirks & Troubleshooting

## Endpoint quirks

| Endpoint | Ghi chú |
|---|---|
| `GET /drafts?filter=draft\|scheduled\|published` | Server-side filter, phải có `offset=0`, `limit` tối đa 25 |
| `POST /drafts` | Tạo draft mới, **bỏ qua `draft_section_id`** trong body. Phải PUT sau |
| `GET /drafts/{id}/prepublish` | Flaky, random 500 với body rỗng. Script bypass — không ảnh hưởng publish |
| `POST /drafts/{id}/publish` với `post_date` tương lai | KHÔNG schedule — publish NGAY. Đừng dùng cho schedule |
| `POST /drafts/{id}/schedule` (python-substack cũ) | 404 — Substack đã bỏ endpoint này |
| `POST /drafts/{id}/scheduled_release` | Endpoint schedule đúng (mới, capture từ DevTools) |
| `DELETE /drafts/{id}/scheduled_release` | Unschedule — chuyển về draft |
| `GET /publication/sections/` | Endpoint sections đúng (python-substack.get_sections() broken) |

## Section: POST bỏ qua, phải PUT

Substack API **bỏ qua** `draft_section_id` trong POST `/drafts` (tạo draft mới). Phải dùng PUT `/drafts/{id}` với body `{"draft_section_id": <id>}` sau khi tạo.

Hai field dễ nhầm trong response:
- `section_id`: luôn `null` cho draft. Không dùng field này.
- `draft_section_id`: field thật chứa section đã gán. Dùng field này để verify.

## Limit tối đa 25

`GET /drafts` reject `limit > 25` với status 400. CLI tự cap về 25 và warn.

## Rate limit

Substack siết rất gắt:
- Mỗi lần khởi tạo `Api(...)` gọi 3-4 request auth (`get_user_profile` + `get_user_publications` + `signin_for_pub`)
- Chạy liên tục 7-8 CLI call → dính `429 Too Many Requests`
- Cooldown 60-120s mới hết
- Không có cách bypass — retry với backoff là lựa chọn duy nhất

## Troubleshooting

**`Must provide email and password, cookies_path, or cookies_string to authenticate.`**
→ Script chạy từ thư mục khác — không tìm thấy `.env`. `cd` vào thư mục chứa `.env` rồi chạy lại.

**`APIError(code=400): Invalid value` ở `list`**
→ Cookie hết hạn hoặc publication URL sai. Lấy cookie mới từ DevTools.

**`APIError(code=500)` ở `prepublish_draft`**
→ Đã wrap try/except, log warning và cho qua. Không ảnh hưởng publish.

**Schedule không xuất hiện ở `list --filter scheduled`**
→ Cookie của publication khác, hoặc chưa refresh. Chờ vài giây rồi thử lại.

**`APIError(code=429): Too Many Requests`**
→ Rate limit. Chờ 60-120s. Xem `batch-operations.md` cho pattern delay + retry.

**Bài lỡ publish thật cần xoá**
→ `python -c "from substack import Api; ...; Api(...).delete_draft(POST_ID)"` — xoá được cả bài published. Không undo.

## ProseMirror bug

`python-substack.Post.from_markdown()` có bug: `parse_inline()` trả dict `{"content": "...", "marks": [...]}` thay vì ProseMirror node hợp lệ. Với bullet_list, dict đi thẳng vào JSON → Substack web báo `RangeError: Invalid input for Fragment.fromJSON`.

Script đã patch bằng `_fix_prosemirror_nodes()` — walk toàn bộ cây, convert dict thiếu `type` thành text node hợp lệ.
