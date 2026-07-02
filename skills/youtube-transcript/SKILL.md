---
name: youtube-transcript
description: >
  Tải transcript (phụ đề/captions) từ YouTube video qua yt-dlp, convert VTT sang plain text sạch (deduplicated).
  Hỗ trợ manual subtitles + auto-generated, 60+ ngôn ngữ, chọn ngôn ngữ cụ thể.

  Dùng khi user chia sẻ YouTube URL và muốn lấy nội dung text, hoặc nói "transcript", "phụ đề", "subtitles",
  "captions", "lấy text từ video", "nội dung video này nói gì", "tải phụ đề", "youtube transcript",
  "chuyển video thành text". Cũng dùng khi user paste link YouTube và muốn đọc/phân tích nội dung video
  mà không cần xem.
---

# YouTube Transcript Downloader

Download transcript from YouTube video, convert to clean plain text.

## Workflow

Follow this exact order. Stop and inform the user if any step fails.

### Step 1: Verify yt-dlp

```bash
command -v yt-dlp
```

If not found, install:

- macOS: `brew install yt-dlp`
- Linux: `sudo apt install -y yt-dlp`
- Fallback: `pip3 install yt-dlp`

If installation fails, tell the user to install manually.

### Step 2: Get video info and check subtitles

```bash
VIDEO_URL="THE_URL"
yt-dlp --print "%(title)s" "$VIDEO_URL"
yt-dlp --list-subs "$VIDEO_URL"
```

Note what's available: manual subtitles (higher quality) vs auto-generated.

### Step 3: Download subtitles

Try in order until one succeeds:

**Manual subtitles (best quality):**

```bash
yt-dlp --write-sub --skip-download --output "transcript_temp" "$VIDEO_URL"
```

**Auto-generated subtitles (fallback):**

```bash
yt-dlp --write-auto-sub --skip-download --output "transcript_temp" "$VIDEO_URL"
```

Both produce a `.vtt` file.

If neither works, inform the user that video này không có phụ đề.

### Step 4: Convert VTT to plain text

Use the bundled conversion script to deduplicate and clean the VTT output:

```bash
VIDEO_TITLE=$(yt-dlp --print "%(title)s" "$VIDEO_URL" | tr '/' '_' | tr ':' '-' | tr '?' '' | tr '"' '')
VTT_FILE=$(ls transcript_temp*.vtt 2>/dev/null | head -n 1)

python3 skills/youtube-transcript/scripts/vtt-to-txt.py "$VTT_FILE" "${VIDEO_TITLE}.txt"
```

Then clean up the temporary VTT file:

```bash
rm "$VTT_FILE"
```

### Step 5: Confirm to user

Tell the user the file name and location. Offer to read/display the content if they want to review it.

## Why deduplication matters

YouTube auto-generated VTT files show captions progressively with overlapping timestamps, producing many duplicate lines. The conversion script uses a seen-set to preserve speaking order while removing duplicates.

## Language selection

By default yt-dlp downloads all available subtitle languages. To target a specific language:

```bash
yt-dlp --write-auto-sub --sub-langs vi --skip-download --output "transcript_temp" "$VIDEO_URL"
```

Common codes: `en` (English), `vi` (Vietnamese), `ja` (Japanese), `ko` (Korean).

## Error handling

Read `references/error-handling.md` for solutions to common issues (private videos, geo-blocking, SSL errors, missing subtitles).
