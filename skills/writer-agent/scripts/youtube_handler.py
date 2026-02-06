#!/usr/bin/env python3
"""Convert YouTube videos to Markdown via transcript.

Usage:
    python youtube_handler.py "https://www.youtube.com/watch?v=VIDEO_ID" [output_dir]

Output: Markdown content with chapters as headings.

Requires: pip install youtube-transcript-api
"""
from __future__ import annotations

import re
import subprocess
from typing import Optional
from urllib.parse import urlparse, parse_qs

# Check dependency
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False

__all__ = ["convert_youtube_to_markdown", "is_youtube_url", "YOUTUBE_AVAILABLE"]


def is_youtube_url(url: str) -> bool:
    """Check if URL is a YouTube video URL.

    Supports:
    - youtube.com/watch?v=ID
    - www.youtube.com/watch?v=ID
    - m.youtube.com/watch?v=ID
    - youtu.be/ID
    """
    if not url.startswith(("http://", "https://")):
        return False

    parsed = urlparse(url)
    hostname = parsed.hostname or ""

    # youtube.com/watch?v=ID
    if hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
        return "/watch" in parsed.path or "/v/" in parsed.path

    # youtu.be/ID
    if hostname == "youtu.be":
        return len(parsed.path) > 1

    return False


def extract_video_id(url: str) -> Optional[str]:
    """Extract video ID from YouTube URL.

    Returns video ID string or None if not found.
    """
    parsed = urlparse(url)
    hostname = parsed.hostname or ""

    # youtu.be/ID
    if hostname == "youtu.be":
        video_id = parsed.path.lstrip("/")
        # Remove any query params or fragments
        return video_id.split("?")[0].split("#")[0] if video_id else None

    # youtube.com/watch?v=ID
    if "youtube.com" in hostname:
        if "/watch" in parsed.path:
            qs = parse_qs(parsed.query)
            return qs.get("v", [None])[0]
        if "/v/" in parsed.path:
            return parsed.path.split("/v/")[1].split("/")[0].split("?")[0]

    return None


def fetch_video_metadata(video_id: str) -> dict:
    """Fetch video title and description via yt-dlp --dump-json.

    Uses single JSON request for all metadata (minimizes API calls).

    Args:
        video_id: YouTube video ID

    Returns:
        dict with: title, description, duration, chapters
    """
    import json as _json

    try:
        # Use yt-dlp --dump-json for single-request metadata fetch
        result = subprocess.run(
            [
                "yt-dlp",
                "--skip-download",
                "--dump-json",
                "--no-warnings",
                f"https://www.youtube.com/watch?v={video_id}"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0 and result.stdout.strip():
            data = _json.loads(result.stdout)
            title = data.get("title", "YouTube Video")
            description = data.get("description", "")
            duration = int(data.get("duration", 0))

            # yt-dlp may provide chapters directly
            yt_chapters = data.get("chapters", [])
            if yt_chapters:
                chapters = [
                    (int(ch.get("start_time", 0)), ch.get("title", ""))
                    for ch in yt_chapters
                    if ch.get("title")
                ]
            else:
                # Parse chapters from description
                chapters = parse_chapters_from_description(description)

            return {
                "title": title,
                "description": description,
                "duration": duration,
                "chapters": chapters
            }
    except subprocess.TimeoutExpired:
        pass
    except FileNotFoundError:
        # yt-dlp not installed
        pass
    except (_json.JSONDecodeError, Exception):
        pass

    # Fallback: try to scrape title and description from page HTML
    title, description = _scrape_youtube_metadata(video_id)
    chapters = parse_chapters_from_description(description) if description else []

    # Use video ID as title if scraping failed (better than generic "YouTube Video")
    if not title:
        title = f"YouTube Video [{video_id}]"

    return {
        "title": title,
        "description": description or "",
        "duration": 0,
        "chapters": chapters
    }


def _scrape_youtube_metadata(video_id: str) -> tuple[Optional[str], Optional[str]]:
    """Fallback: scrape title and description from YouTube page HTML.

    Returns:
        tuple[title, description] - both may be None if scraping fails
    """
    try:
        import urllib.request

        url = f"https://www.youtube.com/watch?v={video_id}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8"
            }
        )

        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read(500000).decode("utf-8", errors="ignore")

            title = None
            description = None

            # Try <title> tag
            title_match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()
                # Clean YouTube suffix
                title = re.sub(r"\s*[-–]\s*YouTube\s*$", "", title, flags=re.IGNORECASE)
                title = title.strip() if title else None

            # Try to extract description from JSON-LD or meta tag
            # Method 1: og:description meta tag
            desc_match = re.search(
                r'<meta\s+(?:property|name)=["\']og:description["\']\s+content=["\']([^"\']+)["\']',
                html, re.IGNORECASE
            )
            if desc_match:
                description = desc_match.group(1).strip()

            # Method 2: Look in ytInitialData JSON
            if not description:
                yt_data_match = re.search(r'var ytInitialData = ({.+?});', html)
                if yt_data_match:
                    try:
                        import json as _json
                        yt_data = _json.loads(yt_data_match.group(1))
                        # Navigate to description
                        desc_runs = (
                            yt_data.get("contents", {})
                            .get("twoColumnWatchNextResults", {})
                            .get("results", {})
                            .get("results", {})
                            .get("contents", [{}])[1]
                            .get("videoSecondaryInfoRenderer", {})
                            .get("attributedDescription", {})
                            .get("content", "")
                        )
                        if desc_runs:
                            description = desc_runs
                    except Exception:
                        pass

            return title, description

    except Exception:
        pass

    return None, None


def _scrape_youtube_title(video_id: str) -> Optional[str]:
    """Fallback: scrape only title from YouTube page HTML.

    Kept for backward compatibility.
    """
    title, _ = _scrape_youtube_metadata(video_id)
    return title


def parse_chapters_from_description(description: str) -> list[tuple[int, str]]:
    """Parse timestamp chapters from video description.

    Formats supported:
    - 00:00 Chapter Title
    - 0:00 Chapter Title
    - 00:00:00 Chapter Title (hours)
    - [00:00] Chapter Title
    - (00:00) Chapter Title

    Returns:
        List of (start_seconds, title) tuples, sorted by time.
    """
    chapters = []

    if not description:
        return chapters

    # Pattern: optional brackets, timestamp (MM:SS or HH:MM:SS), title
    # Matches lines like:
    # 00:00 Mở Đầu
    # [02:26] "Gánh Gánh Gồng Gồng"
    # 01:06:58 Điều gì quan trọng
    pattern = r'[\[\(]?(\d{1,2}):(\d{2})(?::(\d{2}))?[\]\)]?\s+(.+?)(?:\n|$)'

    for match in re.finditer(pattern, description):
        if match.group(3):  # HH:MM:SS format
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = int(match.group(3))
        else:  # MM:SS format
            hours = 0
            minutes = int(match.group(1))
            seconds = int(match.group(2))

        start_seconds = hours * 3600 + minutes * 60 + seconds
        title = match.group(4).strip()

        # Clean title - remove leading punctuation
        title = re.sub(r'^[-–—:]\s*', '', title)

        # Remove trailing URLs or hashtags
        title = re.sub(r'\s*https?://\S+$', '', title)
        title = re.sub(r'\s*#\S+$', '', title)

        if title:
            chapters.append((start_seconds, title))

    # Sort by start time and remove duplicates
    chapters = sorted(set(chapters), key=lambda x: x[0])

    return chapters


def fetch_transcript(video_id: str, languages: list[str] = None) -> list[dict]:
    """Fetch transcript using youtube-transcript-api.

    Args:
        video_id: YouTube video ID
        languages: Preferred languages (default: ['vi', 'en'])

    Returns:
        List of transcript entries with 'text', 'start', 'duration'
    """
    if not YOUTUBE_AVAILABLE:
        raise ImportError("youtube-transcript-api not installed")

    if languages is None:
        languages = ['vi', 'en', 'ja', 'ko', 'zh-Hans', 'zh-Hant', 'fr', 'de', 'es']

    ytt = YouTubeTranscriptApi()

    # Try each language in order
    for lang in languages:
        try:
            transcript = ytt.fetch(video_id, languages=[lang])
            return [
                {"text": e.text, "start": e.start, "duration": e.duration}
                for e in transcript
            ]
        except Exception:
            continue

    # Fallback: get any available transcript
    try:
        transcript_list = ytt.list(video_id)
        if transcript_list:
            # Prefer auto-generated if no manual available
            for t in transcript_list:
                try:
                    transcript = t.fetch()
                    return [
                        {"text": e.text, "start": e.start, "duration": e.duration}
                        for e in transcript
                    ]
                except Exception:
                    continue
    except Exception:
        pass

    return []


def transcript_to_markdown(
    transcript: list[dict],
    chapters: list[tuple[int, str]],
    metadata: dict
) -> str:
    """Convert transcript to structured markdown.

    Args:
        transcript: List of transcript entries with 'text', 'start', 'duration'
        chapters: List of (start_seconds, title) from description
        metadata: Video metadata (title, description, etc.)

    Returns:
        Markdown string with chapters as H2 headings
    """
    title = metadata.get("title", "YouTube Video")

    if not transcript:
        return f"# {title}\n\n> ⚠️ **Không có transcript** cho video này.\n"

    lines = []

    # Title (H1)
    lines.append(f"# {title}")
    lines.append("")

    # If no chapters, create single section
    if not chapters:
        chapters = [(0, "Nội dung")]

    # Add chapter end times for easier lookup
    chapter_ranges = []
    for i, (start, title_text) in enumerate(chapters):
        end = chapters[i + 1][0] if i + 1 < len(chapters) else float('inf')
        chapter_ranges.append((start, end, title_text))

    # Group transcript entries by chapter
    current_chapter_idx = 0
    current_para = []
    chapter_started = False

    for entry in transcript:
        start = entry["start"]
        text = entry["text"].strip()

        # Skip noise markers
        if text.lower() in ["[âm nhạc]", "[music]", "[applause]", "[vỗ tay]", ""]:
            continue

        # Find which chapter this entry belongs to
        while current_chapter_idx < len(chapter_ranges) - 1:
            _, end, _ = chapter_ranges[current_chapter_idx]
            if start >= end:
                # Output current paragraph before moving to next chapter
                if current_para:
                    lines.append(" ".join(current_para))
                    lines.append("")
                    current_para = []

                current_chapter_idx += 1
                chapter_started = False
            else:
                break

        # Output chapter heading if not done yet
        if not chapter_started:
            _, _, chapter_title = chapter_ranges[current_chapter_idx]
            lines.append(f"## {chapter_title}")
            lines.append("")
            chapter_started = True

        # Add text to current paragraph
        current_para.append(text)

        # Break paragraph every ~10 entries for readability
        if len(current_para) >= 10:
            lines.append(" ".join(current_para))
            lines.append("")
            current_para = []

    # Output remaining paragraph
    if current_para:
        lines.append(" ".join(current_para))
        lines.append("")

    return "\n".join(lines)


def convert_youtube_to_markdown(url: str) -> tuple[str, dict]:
    """Convert YouTube video to Markdown via transcript.

    Args:
        url: YouTube video URL

    Returns:
        tuple[str, dict]: (markdown_content, metadata)
            metadata contains: title, description, duration, chapters, video_id, url, word_count

    Raises:
        ValueError: If not a valid YouTube URL
        ImportError: If youtube-transcript-api not installed
    """
    if not is_youtube_url(url):
        raise ValueError(f"Not a YouTube URL: {url}")

    if not YOUTUBE_AVAILABLE:
        raise ImportError("YouTube support requires: uv pip install youtube-transcript-api")

    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError(f"Could not extract video ID from: {url}")

    # Fetch metadata (title, description, chapters)
    metadata = fetch_video_metadata(video_id)
    metadata["video_id"] = video_id
    metadata["url"] = url

    # Fetch transcript
    transcript = fetch_transcript(video_id)

    if not transcript:
        # Return minimal content with warning
        markdown = f"# {metadata.get('title', 'YouTube Video')}\n\n"
        markdown += f"> ⚠️ **Không có transcript** cho video này.\n\n"
        markdown += f"Video URL: {url}\n"
        metadata["warning"] = "No transcript available"
        metadata["word_count"] = len(markdown.split())
        metadata["has_chapters"] = False
        return markdown, metadata

    # Convert to markdown
    markdown = transcript_to_markdown(
        transcript,
        metadata.get("chapters", []),
        metadata
    )

    # Update metadata
    metadata["word_count"] = len(markdown.split())
    metadata["has_chapters"] = len(metadata.get("chapters", [])) > 0
    metadata["transcript_entries"] = len(transcript)

    return markdown, metadata


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        print("Usage: python youtube_handler.py <youtube_url>")
        sys.exit(1)

    if not YOUTUBE_AVAILABLE:
        print("Error: YouTube support requires: uv pip install youtube-transcript-api")
        sys.exit(2)

    url = sys.argv[1]

    try:
        content, meta = convert_youtube_to_markdown(url)
        print(f"Title: {meta.get('title')}")
        print(f"Video ID: {meta.get('video_id')}")
        print(f"Duration: {meta.get('duration')}s")
        print(f"Chapters: {len(meta.get('chapters', []))}")
        print(f"Transcript entries: {meta.get('transcript_entries', 0)}")
        print(f"Word count: {meta.get('word_count')}")

        if meta.get("warning"):
            print(f"Warning: {meta.get('warning')}")

        print("\n--- Preview (first 1000 chars) ---\n")
        print(content[:1000])

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, indent=2))
        sys.exit(1)
