#!/usr/bin/env python3
"""Scan và crawl bài viết từ newsletter Substack khác.

Không cần auth — dùng public RSS feed + JSON API (/api/v1/).
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import json
import random
import re
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import feedparser
import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify as md


@dataclass
class FeedEntry:
    title: str
    url: str
    date: str
    excerpt: str
    author: str
    publication: str
    read_time: str = ""


@dataclass
class CrawledPost:
    title: str
    url: str
    date: str
    author: str
    publication: str
    body_md: str
    tags: list[str] = field(default_factory=list)


_API_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
}


def _pub_url(slug: str) -> str:
    return f"https://{slug}.substack.com"


def normalize_slug(slug_or_url: str) -> str:
    """Chuẩn hoá input → slug (phần trước .substack.com)."""
    s = slug_or_url.strip().rstrip("/")
    if "." in s or "/" in s:
        parsed = urlparse(s if "://" in s else f"https://{s}")
        host = parsed.hostname or ""
        if ".substack.com" in host:
            return host.split(".")[0]
        return host.replace("www.", "")
    return s


def _feed_url(slug: str) -> str:
    return f"https://{slug}.substack.com/feed"


def _estimate_read_time(text: str) -> str:
    words = len(text.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min"


def fetch_feed(slug: str, limit: int = 10) -> list[FeedEntry]:
    slug = normalize_slug(slug)
    url = _feed_url(slug)
    feed = feedparser.parse(url)

    if feed.bozo and not feed.entries:
        raise RuntimeError(f"Không parse được RSS từ {url}: {feed.bozo_exception}")

    pub_title = feed.feed.get("title", slug)
    entries: list[FeedEntry] = []

    for e in feed.entries[:limit]:
        date_str = ""
        if hasattr(e, "published_parsed") and e.published_parsed:
            date_str = time.strftime("%Y-%m-%d", e.published_parsed)

        excerpt = ""
        if hasattr(e, "summary"):
            soup = BeautifulSoup(e.summary, "html.parser")
            excerpt = soup.get_text(strip=True)[:200]

        read_time = _estimate_read_time(excerpt) if excerpt else ""

        entries.append(
            FeedEntry(
                title=e.get("title", "(no title)"),
                url=e.get("link", ""),
                date=date_str,
                excerpt=excerpt,
                author=e.get("author", ""),
                publication=pub_title,
                read_time=read_time,
            )
        )
    return entries


def fetch_archive(slug: str, limit: int | None = None) -> list[FeedEntry]:
    """Lấy danh sách bài qua /api/v1/archive — trả TẤT CẢ bài, không giới hạn 25 như RSS."""
    slug = normalize_slug(slug)
    base = _pub_url(slug)
    entries: list[FeedEntry] = []
    offset = 0
    page_size = 12

    while True:
        resp = httpx.get(
            f"{base}/api/v1/archive",
            params={"sort": "new", "offset": offset, "limit": page_size},
            headers={**_API_HEADERS, "Referer": f"{base}/archive"},
            follow_redirects=True,
            timeout=30,
        )
        resp.raise_for_status()
        posts = resp.json()
        if not posts:
            break

        for p in posts:
            date_str = ""
            if p.get("post_date"):
                try:
                    date_str = datetime.fromisoformat(
                        p["post_date"].replace("Z", "+00:00")
                    ).strftime("%Y-%m-%d")
                except ValueError:
                    date_str = p["post_date"][:10]

            excerpt = p.get("description") or p.get("truncated_body_text", "")
            wc = p.get("wordcount") or 0
            read_time = f"{max(1, round(wc / 200))} min" if wc else ""

            entries.append(
                FeedEntry(
                    title=p.get("title") or "(no title)",
                    url=f"{base}/p/{p.get('slug', '')}",
                    date=date_str,
                    excerpt=excerpt[:200],
                    author=p.get("publishedBylines", [{}])[0].get("name", "")
                    if p.get("publishedBylines")
                    else "",
                    publication=p.get("publication", {}).get("name", slug),
                    read_time=read_time,
                )
            )

        offset += len(posts)
        if limit and len(entries) >= limit:
            entries = entries[:limit]
            break
        if len(posts) < page_size:
            break
        time.sleep(1.0 + random.random())

    return entries


def crawl_post_api(post_slug: str, pub_slug: str) -> CrawledPost:
    """Lấy full bài qua /api/v1/posts/{slug} — structured data, không cần parse HTML."""
    base = _pub_url(pub_slug)
    resp = httpx.get(
        f"{base}/api/v1/posts/{post_slug}",
        headers={**_API_HEADERS, "Referer": f"{base}/archive"},
        follow_redirects=True,
        timeout=30,
    )
    resp.raise_for_status()
    d = resp.json()

    date_str = ""
    if d.get("post_date"):
        try:
            date_str = datetime.fromisoformat(
                d["post_date"].replace("Z", "+00:00")
            ).strftime("%Y-%m-%d")
        except ValueError:
            date_str = d["post_date"][:10]

    body_html = d.get("body_html") or ""
    body_md = md(body_html, heading_style="ATX", strip=["img"]) if body_html else ""
    body_md = re.sub(r"\n{3,}", "\n\n", body_md).strip()

    author = ""
    if d.get("publishedBylines"):
        author = d["publishedBylines"][0].get("name", "")

    raw_tags = d.get("postTags") or []
    tags = [
        (t if isinstance(t, str) else t.get("name", "")).lower()
        for t in raw_tags
        if t
    ]

    pub_name = d.get("publication", {}).get("name", pub_slug)

    return CrawledPost(
        title=d.get("title") or "(no title)",
        url=f"{base}/p/{post_slug}",
        date=date_str,
        author=author,
        publication=pub_name,
        body_md=body_md,
        tags=tags,
    )


def crawl_post(url: str) -> CrawledPost:
    resp = httpx.get(url, follow_redirects=True, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    title_el = soup.select_one("h1.post-title") or soup.find("h1")
    title = title_el.get_text(strip=True) if title_el else "(no title)"

    body_el = soup.select_one("div.body.markup") or soup.select_one("div.available-content")
    body_md = md(str(body_el), heading_style="ATX", strip=["img"]) if body_el else ""
    body_md = re.sub(r"\n{3,}", "\n\n", body_md).strip()

    author = ""
    author_el = soup.select_one("a.frontend-pencraft-Text-module__decoration-hover-underline--BEYAn")
    if not author_el:
        author_el = soup.select_one("div.pencraft span a")
    if author_el:
        author = author_el.get_text(strip=True)

    date_str = ""
    time_el = soup.select_one("time") or soup.select_one("div.pencraft time")
    if time_el:
        dt_attr = time_el.get("datetime", "")
        if dt_attr:
            try:
                date_str = datetime.fromisoformat(dt_attr.replace("Z", "+00:00")).strftime("%Y-%m-%d")
            except ValueError:
                date_str = dt_attr[:10]
        else:
            date_str = time_el.get_text(strip=True)

    pub = ""
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if ".substack.com" in host:
        pub = host.split(".")[0]
    pub_el = soup.select_one("a.navbar-title-link span") or soup.select_one("h2.navbar-title")
    if pub_el:
        pub = pub_el.get_text(strip=True)

    tags: list[str] = []
    for tag_el in soup.select("a.post-tag, a[data-testid='tag']"):
        t = tag_el.get_text(strip=True)
        if t:
            tags.append(t.lower())

    return CrawledPost(
        title=title,
        url=url,
        date=date_str,
        author=author,
        publication=pub,
        body_md=body_md,
        tags=tags,
    )


def _slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"[-\s]+", "-", s)[:80]


def save_post(post: CrawledPost, output_dir: Path) -> Path | None:
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = _slugify(post.title)
    date_prefix = post.date or "undated"
    filename = f"{date_prefix}-{slug}.md"
    filepath = output_dir / filename

    if filepath.exists():
        print(f"SKIP (đã tồn tại): {filepath}")
        return None

    tags_yaml = ", ".join(post.tags) if post.tags else ""
    frontmatter = (
        f"---\n"
        f'title: "{post.title}"\n'
        f'author: "{post.author}"\n'
        f'date: "{post.date}"\n'
        f'url: "{post.url}"\n'
        f'publication: "{post.publication}"\n'
        f"tags: [{tags_yaml}]\n"
        f"---\n\n"
    )
    filepath.write_text(frontmatter + post.body_md, encoding="utf-8")
    print(f"SAVED: {filepath}")
    return filepath


def crawl_feed(
    slug: str, limit: int = 5, output_dir: Path = Path("./crawled"), delay: float = 2.0
) -> list[Path]:
    entries = fetch_feed(slug, limit=limit)
    saved: list[Path] = []
    for i, entry in enumerate(entries):
        try:
            post = crawl_post(entry.url)
            result = save_post(post, output_dir)
            if result:
                saved.append(result)
        except Exception as e:
            print(f"ERR crawl {entry.url}: {e}")
        if i < len(entries) - 1:
            time.sleep(delay + random.random() * 2.0)
    return saved


def crawl_archive(
    slug: str,
    limit: int | None = None,
    output_dir: Path = Path("./crawled"),
    delay_base: float = 2.0,
    delay_jitter: float = 3.0,
) -> list[Path]:
    """Crawl tất cả bài qua archive API + post API — không giới hạn 25 như RSS."""
    slug = normalize_slug(slug)
    entries = fetch_archive(slug, limit=limit)
    total = len(entries)
    print(f"Tìm thấy {total} bài từ {slug}")

    saved: list[Path] = []
    for i, entry in enumerate(entries):
        post_slug = entry.url.rstrip("/").split("/")[-1]
        try:
            post = crawl_post_api(post_slug, slug)
            result = save_post(post, output_dir)
            if result:
                saved.append(result)
                print(f"  [{i + 1}/{total}] {entry.title}")
        except Exception as e:
            print(f"  ERR [{i + 1}/{total}] {entry.title}: {e}")
        if i < total - 1:
            time.sleep(delay_base + random.random() * delay_jitter)
    return saved


def print_feed_table(entries: list[FeedEntry]) -> None:
    if not entries:
        print("Không có bài nào.")
        return
    print(f"{'#':>3}  {'Ngày':10}  {'Tác giả':20}  {'Tiêu đề'}")
    print("-" * 80)
    for i, e in enumerate(entries, 1):
        author = (e.author[:18] + "..") if len(e.author) > 20 else e.author
        print(f"{i:3}  {e.date:10}  {author:20}  {e.title}")
    print(f"\nTổng: {len(entries)} bài từ {entries[0].publication}")


def print_feed_json(entries: list[FeedEntry]) -> None:
    print(json.dumps([asdict(e) for e in entries], indent=2, ensure_ascii=False))
