---
name: pexels-media
description: "Tìm/tải ảnh, video Pexels miễn phí bản quyền. Tạo metadata sidecar. Trigger: stock media, hero image, placeholder."
---

# Pexels Media Sourcing

Source high-quality, royalty-free images and videos from Pexels for design work, placeholders, or content creation.

## Prerequisites

This skill requires the `PEXELS_API_KEY` environment variable to be set.

```bash
echo $PEXELS_API_KEY
```

If not set, obtain a free API key from [https://www.pexels.com/api/](https://www.pexels.com/api/)

## API Base URLs

- Photos: `https://api.pexels.com/v1/`
- Videos: `https://api.pexels.com/videos/`

## Authentication

All requests require the Authorization header:

```bash
curl -H "Authorization: $PEXELS_API_KEY" "https://api.pexels.com/v1/search?query=nature"
```

## Photo Endpoints

### Search Photos

```bash
curl -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/search?query=QUERY&orientation=ORIENTATION&size=SIZE&color=COLOR&locale=LOCALE&page=PAGE&per_page=PER_PAGE"
```

| Parameter     | Required | Values                                                                                                                    |
| ------------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| `query`       | Yes      | Search term                                                                                                               |
| `orientation` | No       | `landscape`, `portrait`, `square`                                                                                         |
| `size`        | No       | `large` (24MP), `medium` (12MP), `small` (4MP)                                                                            |
| `color`       | No       | `red`, `orange`, `yellow`, `green`, `turquoise`, `blue`, `violet`, `pink`, `brown`, `black`, `gray`, `white`, or hex code |
| `locale`      | No       | `en-US`, `pt-BR`, `es-ES`, `de-DE`, `fr-FR`, `ja-JP`, `zh-CN`, `ko-KR`, etc.                                              |
| `page`        | No       | Page number (default: 1)                                                                                                  |
| `per_page`    | No       | Results per page (default: 15, max: 80)                                                                                   |


### Curated Photos

Trending photos curated by the Pexels team (updated hourly):

```bash
curl -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/curated?page=1&per_page=15"
```

### Get Photo by ID

```bash
curl -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/photos/PHOTO_ID"
```

## Video Endpoints

### Search Videos

```bash
curl -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/videos/search?query=QUERY&orientation=ORIENTATION&size=SIZE&min_width=MIN_WIDTH&min_height=MIN_HEIGHT&min_duration=MIN_DURATION&max_duration=MAX_DURATION&page=PAGE&per_page=PER_PAGE"
```

| Parameter      | Description                 |
| -------------- | --------------------------- |
| `min_width`    | Minimum width in pixels     |
| `min_height`   | Minimum height in pixels    |
| `min_duration` | Minimum duration in seconds |
| `max_duration` | Maximum duration in seconds |


### Popular Videos

```bash
curl -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/videos/popular?min_width=1920&min_duration=10&max_duration=60&page=1&per_page=15"
```

### Get Video by ID

```bash
curl -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/videos/videos/VIDEO_ID"
```

## Collections

### Featured Collections

```bash
curl -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/collections/featured?page=1&per_page=15"
```

### Collection Media

```bash
curl -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/collections/COLLECTION_ID?type=TYPE&page=1&per_page=15"
```

Type parameter: `photos`, `videos`, or omit for both.

## Photo Sizes Available

| Key         | Description                            |
| ----------- | -------------------------------------- |
| `original`  | Original size uploaded by photographer |
| `large2x`   | Width 940px, height doubled            |
| `large`     | Width 940px                            |
| `medium`    | Height 350px                           |
| `small`     | Height 130px                           |
| `portrait`  | Width 800px, height 1200px             |
| `landscape` | Width 1200px, height 627px             |
| `tiny`      | Width 280px, height 200px              |


## Video Files Available

| Quality | Typical Resolution         |
| ------- | -------------------------- |
| `hd`    | 1280x720                   |
| `sd`    | 640x360                    |
| `hls`   | Adaptive streaming         |
| Various | Full HD, 4K when available |


## MANDATORY: Sidecar Metadata Files

For EVERY downloaded file, create a sidecar metadata file. This ensures proper attribution tracking and reuse.

### Naming Convention

For `mountain-sunset.jpg`, create `mountain-sunset.jpg.meta.json`.

### Photo Sidecar Content

```json
{
  "source": "pexels",
  "type": "photo",
  "id": 12345,
  "url": "https://www.pexels.com/photo/12345/",
  "download_url": "https://images.pexels.com/photos/12345/pexels-photo-12345.jpeg",
  "downloaded_size": "large",
  "width": 1920,
  "height": 1080,
  "photographer": "John Doe",
  "photographer_url": "https://www.pexels.com/@johndoe",
  "photographer_id": 67890,
  "avg_color": "#7E5835",
  "alt": "Brown mountain during sunset",
  "license": "Pexels License - Free for personal and commercial use",
  "attribution": "Photo by John Doe on Pexels",
  "attribution_html": "<a href=\"https://www.pexels.com/photo/12345/\">Photo</a> by <a href=\"https://www.pexels.com/@johndoe\">John Doe</a> on <a href=\"https://www.pexels.com\">Pexels</a>",
  "downloaded_at": "2025-12-02T14:30:00Z",
  "api_response": {}
}
```

### Video Sidecar Content

```json
{
  "source": "pexels",
  "type": "video",
  "id": 12345,
  "url": "https://www.pexels.com/video/12345/",
  "download_url": "https://videos.pexels.com/video-files/12345/...",
  "downloaded_quality": "hd",
  "width": 1920,
  "height": 1080,
  "duration": 30,
  "user": {
    "id": 67890,
    "name": "John Doe",
    "url": "https://www.pexels.com/@johndoe"
  },
  "video_files": [],
  "video_pictures": [],
  "license": "Pexels License - Free for personal and commercial use",
  "attribution": "Video by John Doe on Pexels",
  "downloaded_at": "2025-12-02T14:30:00Z",
  "api_response": {}
}
```

## Download Workflow

### 1. Search and Select

```bash
RESPONSE=$(curl -s -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/search?query=office+workspace&orientation=landscape&per_page=5")

echo "$RESPONSE" | jq '.photos[] | {id, photographer, alt, url: .src.large}'
```

### 2. Download with Sidecar

```bash
PHOTO_ID=12345
PHOTO_DATA=$(curl -s -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/photos/$PHOTO_ID")

DOWNLOAD_URL=$(echo "$PHOTO_DATA" | jq -r '.src.large')
FILENAME="pexels-$PHOTO_ID-large.jpg"

curl -L -o "$FILENAME" "$DOWNLOAD_URL"

echo "$PHOTO_DATA" | jq '{
  source: "pexels",
  type: "photo",
  id: .id,
  url: .url,
  download_url: .src.large,
  downloaded_size: "large",
  width: .width,
  height: .height,
  photographer: .photographer,
  photographer_url: .photographer_url,
  photographer_id: .photographer_id,
  avg_color: .avg_color,
  alt: .alt,
  license: "Pexels License - Free for personal and commercial use",
  attribution: ("Photo by " + .photographer + " on Pexels"),
  downloaded_at: (now | todate),
  api_response: .
}' > "$FILENAME.meta.json"
```

### 3. Download Video with Sidecar

```bash
VIDEO_ID=12345
VIDEO_DATA=$(curl -s -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/videos/videos/$VIDEO_ID")

DOWNLOAD_URL=$(echo "$VIDEO_DATA" | jq -r '.video_files[] | select(.quality=="hd") | .link' | head -1)
FILENAME="pexels-$VIDEO_ID-hd.mp4"

curl -L -o "$FILENAME" "$DOWNLOAD_URL"

echo "$VIDEO_DATA" | jq '{
  source: "pexels",
  type: "video",
  id: .id,
  url: .url,
  download_url: (.video_files[] | select(.quality=="hd") | .link),
  downloaded_quality: "hd",
  width: .width,
  height: .height,
  duration: .duration,
  user: .user,
  video_files: .video_files,
  video_pictures: .video_pictures,
  license: "Pexels License - Free for personal and commercial use",
  attribution: ("Video by " + .user.name + " on Pexels"),
  downloaded_at: (now | todate),
  api_response: .
}' > "$FILENAME.meta.json"
```

## Rate Limits

- 200 requests/hour, 20,000 requests/month
- Check response headers: `X-Ratelimit-Limit`, `X-Ratelimit-Remaining`, `X-Ratelimit-Reset`

## Attribution

While not legally required by the Pexels license, attribution is encouraged:

- Minimal: "Photo by [Photographer] on Pexels"
- With link: "Photo by [Photographer](photographer_url) on [Pexels](photo_url)"
- HTML: Use the `attribution_html` from the sidecar file

## Example Use Cases

### Placeholder Images for UI Design

```bash
curl -s -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/search?query=minimal+abstract&orientation=square&size=small&per_page=5"
```

### Hero Background Video

```bash
curl -s -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/videos/search?query=nature+aerial&orientation=landscape&min_width=1920&min_duration=5&max_duration=15"
```

### Product Photography Backgrounds

```bash
curl -s -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/search?query=white+background+texture&color=white&size=large"
```

## Checklist

When using this skill:

- [ ] Verify `PEXELS_API_KEY` is set
- [ ] Choose appropriate endpoint (search, curated, popular, collection)
- [ ] Apply relevant filters (orientation, size, color, duration)
- [ ] Select appropriate resolution for use case
- [ ] Download file to appropriate location
- [ ] CREATE SIDECAR METADATA FILE (mandatory for every download)
- [ ] Consider attribution in final use
