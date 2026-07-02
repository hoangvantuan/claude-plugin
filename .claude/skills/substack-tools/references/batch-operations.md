# Batch Operations

## Rate limit

Chạy nhiều CLI call liên tiếp không delay → dính 429 sau ~7 call. Cooldown ~90s.

Nguồn 429 chính: **fetch_sections()** và **khởi tạo Api()** (3-4 request auth mỗi lần). Giảm 429 bằng cách cache kết quả, không gọi lặp.

## Pattern 1: Bash shell (đơn giản, mỗi bài 1 CLI call)

```bash
#!/bin/bash
PY=~/.venv/claude/bin/python
SCRIPT=<path-to>/substack_cli.py

run_one() {
  local path="$1" cover="$2" at="$3" label="$4"
  for attempt in 1 2 3 4 5; do
    if $PY $SCRIPT schedule "$path" "$cover" --at "$at"; then
      return 0
    fi
    echo "[$label] retry $attempt sau 60s"
    sleep 60
  done
  echo "[$label] FAILED"
  return 1
}

run_one "{article-path}" "{cover-path}" "{datetime+tz}" "1"
sleep 8
run_one "{article-path}" "{cover-path}" "{datetime+tz}" "2"
sleep 8
```

Nhược điểm: mỗi call khởi tạo `Api()` mới (3-4 request auth), tốn quota rate limit.

## Pattern 2: Python script (tối ưu, 1 Api instance cho cả batch)

Dùng khi batch > 5 bài, cần custom slug, gán section, hoặc thêm nội dung động (cross-link, TOC, ...).

Ưu điểm so với pattern 1:
- 1 `Api()` instance duy nhất, tiết kiệm auth request
- Cache `section_id` 1 lần, không gọi `fetch_sections()` lặp
- Combine slug + section trong 1 PUT call
- Delay 5s đủ (thay vì 8s) vì ít request hơn

### Setup 1 lần

```python
cookie, _ = load_env()
api = Api(cookies_string=cookie, publication_url=PUBLICATION_URL)
user_id = api.get_user_id()
section_id = resolve_section_id(api, SECTION_NAME)  # cache, KHÔNG gọi lặp
```

### Loop cơ bản

```python
for article in articles:
    result = api.post_draft(payload)
    api._session.put(f"{api.publication_url}/drafts/{result['id']}",
                     json={"slug": slug, "draft_section_id": section_id})
    _schedule_draft_raw(api, result["id"], schedule_dt, "everyone")
    time.sleep(5)
```

Lưu ý: `api._session.put()` là internal API của python-substack, không phải public method. Dùng vì `post_draft()` bỏ qua `draft_section_id` và slug.

### Optional: custom slug

Substack tự sinh slug xấu. Set trước khi schedule (xem `api-quirks.md` mục "Custom slug").

Combine slug + section trong 1 PUT call để giảm request:

```python
api._session.put(f"{api.publication_url}/drafts/{draft_id}",
    json={"slug": "{custom-slug}", "draft_section_id": section_id})
```

### Optional: cross-link giữa các bài

Khi batch là loạt bài liên quan, có thể thêm mục lục hoặc link chéo. Cần biết slug trước → build link → append vào body trước khi tạo draft.

```python
links = []
for article in articles:
    url = f"https://{publication}/p/{article['slug']}"
    links.append(f"- [{article['title']}]({url})")
cross_link_md = "\n".join(links)
```

Append `cross_link_md` vào cuối body mỗi bài trước `post_draft()`.

### Recovery khi 429 giữa chừng

Ghi lại bài đã hoàn thành, chờ 2 phút, chạy lại script với skip logic:

```python
DONE = {"{id-1}", "{id-2}"}  # draft ID đã xong

for article in articles:
    if article["id"] in DONE:
        continue
    # ... tiếp tục xử lý
```

## Checklist trước khi chạy batch

- Mapping: danh sách bài, path article, path cover, ngày đăng
- File tồn tại: article và cover
- Section name đúng (nếu gán section)
- Custom slug cho mỗi bài (nếu cần)
- Delay: 5s (Python) hoặc 8s (Bash)

## Lưu ý quan trọng

1. **Cache section_id**: gọi 1 lần duy nhất. Gọi mỗi bài → 429 sau bài thứ 7.
2. **Retry tối đa 5 lần**, mỗi lần chờ 60s.
3. **Không sửa `substack_cli.py` khi batch đang chạy**.
4. **Log ra file**: `2>&1 | tee batch.log`.
5. **Verify sau batch**: `get_draft(id)` từng bài. `list --filter scheduled` có thể trả rỗng cho publication phụ.
6. **`list --limit` tối đa 25**: Substack API reject limit > 25 với status 400.
