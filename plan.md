# Plan: Thêm tính năng scan & crawl newsletter cho substack-tools

## Context

Skill `substack-tools` hiện chỉ quản lý bài viết trên newsletter CỦA MÌNH (draft, schedule, publish, list). User muốn thêm khả năng scan/crawl bài viết từ newsletter KHÁC trên Substack — để tham khảo ý tưởng, content curation, và phân tích đối thủ.

Platform: chỉ Substack. Output: Markdown files.

## Thay đổi

### 1. Tạo file mới: `skills/substack-tools/scripts/substack_crawl.py` (~180 lines)

Module chứa toàn bộ logic scan/crawl, không cần auth.

**Data classes:**
- `FeedEntry` — metadata 1 bài từ RSS (title, url, date, excerpt, read_time, author, publication)
- `CrawledPost` — bài đầy đủ kèm markdown body

**Hàm chính:**
- `normalize_slug(slug_or_url)` — chuẩ hoá input (slug, full URL, domain) → slug
- `fetch_feed(slug, limit)` — parse RSS → list[FeedEntry]
- `crawl_post(url)` — fetch + parse 1 bài → CrawledPost
- `crawl_feed(slug, limit, output_dir, delay)` — batch crawl từ RSS feed
- `save_post(post, output_dir)` — lưu .md với YAML frontmatter
- `print_feed_table(entries)` / `print_feed_json(entries)` — hiển thị kết quả

**Dependencies mới:** `feedparser`, `httpx`, `beautifulsoup4`, `markdownify`

**Output format:**
```yaml
---
title: "How to Think"
author: "John Doe"
date: "2026-04-15"
url: "https://example.substack.com/p/how-to-think"
publication: "Example"
tags: [thinking, philosophy]
---
<markdown body>
```

Filename: `{YYYY-MM-DD}-{slug}.md`. Skip nếu file đã tồn tại.

### 2. Sửa: `skills/substack-tools/scripts/substack_cli.py` (+80 lines)

Thêm 3 subcommand mới vào `build_parser()` (sau line 528):

- **`scan <slug>`** — quét RSS feed, hiện bảng bài viết
  - `--limit N` (default 10), `--json`
- **`crawl <url>`** — tải 1 bài thành .md
  - `--output-dir` (default ./crawled)
- **`crawl-feed <slug>`** — batch tải N bài từ publication
  - `--limit N` (default 5), `--output-dir`

3 handler function ngắn (~15 lines mỗi cái), import từ `substack_crawl`. Guard `_CRAWL_AVAILABLE` cho missing deps.

### 3. Sửa: `skills/substack-tools/SKILL.md`

Thêm dependency install line, 3 command docs mới, update ranh giới hành động (scan/crawl = read-only, tự làm được).

### 4. Tạo: `skills/substack-tools/references/crawl-guide.md` (~50 lines)

Troubleshooting: HTML selectors, rate limiting, paywall handling, RSS quirks.

### 5. Sửa: `CLAUDE.md`

Update mô tả substack-tools trong bảng skill.

## Thứ tự thực hiện

1. Install dependencies
2. Tạo `substack_crawl.py`
3. Sửa `substack_cli.py` thêm 3 subcommand
4. Cập nhật `SKILL.md`
5. Tạo `references/crawl-guide.md`
6. Cập nhật `CLAUDE.md`

## Verify

```bash
# 1. Dependencies
~/.venv/claude/bin/python -c "import feedparser, httpx, bs4, markdownify; print('OK')"

# 2. Scan
~/.venv/claude/bin/python skills/substack-tools/scripts/substack_cli.py scan meaningquiry --limit 3

# 3. Crawl 1 bài
~/.venv/claude/bin/python skills/substack-tools/scripts/substack_cli.py crawl <URL> --output-dir /tmp/test-crawl

# 4. Crawl-feed batch
~/.venv/claude/bin/python skills/substack-tools/scripts/substack_cli.py crawl-feed meaningquiry --limit 2 --output-dir /tmp/test-crawl

# 5. Idempotency: chạy lại → skip file đã có
```
