# Crawl Guide — Troubleshooting & Notes

## Hai chế độ lấy dữ liệu

| Chế độ | Cách dùng | Nguồn dữ liệu | Giới hạn |
| ------ | --------- | -------------- | -------- |
| Mặc định | `scan` / `crawl-feed` | RSS feed + HTML scrape | ~25 bài mới nhất |
| `--all` | `scan --all` / `crawl-feed --all` | Archive API + Post API (`/api/v1/`) | Tất cả bài đã publish |

Khi dùng `--all`, CLI gọi 2 endpoint public (không cần auth):

- `GET /api/v1/archive?sort=new&offset=N&limit=12` — paginate danh sách bài
- `GET /api/v1/posts/{slug}` — lấy full body_html, tags, word count

## Rate Limiting

Chiến lược delay tự động (giống browser thật — random jitter, không request đều đặn):

| Thao tác | Delay |
| -------- | ----- |
| `fetch_archive` (list từng trang) | 1-2s giữa mỗi trang |
| `crawl_feed` (RSS mode) | 2-4s giữa mỗi bài |
| `crawl_archive` (`--all` mode) | 2-5s giữa mỗi bài |

Nếu gặp 429 hoặc bị block: tăng `delay_base` / `delay_jitter` trong `crawl_archive()`.

## HTML Selectors (chế độ RSS)

Chỉ dùng khi crawl qua HTML (không dùng `--all`). Substack thay đổi class name theo thời gian. Selector hiện tại (04/2026):

| Phần tử | Selector chính | Fallback |
| ------- | -------------- | -------- |
| Tiêu đề | `h1.post-title` | `h1` |
| Body | `div.body.markup` | `div.available-content` |
| Tác giả | `a.frontend-pencraft-Text-module__decoration-hover-underline--BEYAn` | `div.pencraft span a` |
| Ngày | `time[datetime]` | `div.pencraft time` |
| Tags | `a.post-tag` | `a[data-testid='tag']` |

Nếu crawl trả body rỗng → Substack đã đổi selector. Cập nhật `crawl_post()` trong `substack_crawl.py`.

Chế độ `--all` dùng JSON API nên **không phụ thuộc HTML selector** — ưu tiên dùng `--all` khi cần dữ liệu ổn định.

## RSS Feed

- URL pattern: `https://<slug>.substack.com/feed`
- Custom domain: RSS thường redirect về `.substack.com/feed` — `feedparser` xử lý tự động
- Feed trả tối đa ~20-25 entry gần nhất (giới hạn Substack, không thay đổi được)
- Nếu feed parse fail: kiểm tra slug đúng chưa, newsletter có public không

## Paywall / Subscriber-only

- RSS chỉ chứa excerpt cho bài subscriber-only
- API (`--all`) trả `body_html` phần public (trước paywall gate)
- Không có cách bypass — đây là giới hạn thiết kế

## Output Format

File `.md` lưu với YAML frontmatter:

```yaml
---
title: "Tiêu đề bài"
author: "Tên tác giả"
date: "2026-04-15"
url: "https://example.substack.com/p/slug"
publication: "Example"
tags: [tag1, tag2]
---
<markdown body>
```

Filename: `{YYYY-MM-DD}-{slugified-title}.md`. Chạy lại sẽ skip file đã tồn tại.

## Custom Domain

Newsletter dùng custom domain (không phải `*.substack.com`):

- `scan`: truyền slug gốc (vd: `platformer`), không truyền custom domain
- `crawl`: truyền full URL bài viết — hoạt động với cả custom domain
