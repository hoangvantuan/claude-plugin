# Size guide for gpt-image-2

## Technical constraints

- Max edge: 3840 px
- Both edges must be multiples of 16
- Max aspect ratio: 3:1
- Total pixels: 655,360 to 8,294,400

## Common sizes

### Square (1:1)

| Size | Total pixels | Use case |
|-----------|------------|----------|
| 816x816 | 666K | Smallest valid size (quick drafts — on the fallback CLI, `--quality low` is faster than shrinking the size) |
| 1024x1024 | 1M | Icon, avatar, social post — fastest in practice |
| 2048x2048 | 4.2M | High-quality print |

### Landscape

| Size | Ratio | Use case |
|-----------|--------|----------|
| 1536x1024 | 3:2 | Standard landscape image |
| 1792x1024 | 7:4 | Website banner |
| 1920x1080 | 16:9 | YouTube thumbnail, wallpaper |
| 2560x1440 | 16:9 | QHD wallpaper |
| 3840x2160 | 16:9 | 4K wallpaper |

### Portrait

| Size | Ratio | Use case |
|-----------|--------|----------|
| 1024x1536 | 2:3 | Story, vertical poster |
| 1024x1792 | 4:7 | Mobile wallpaper |
| 1088x1920 | ~9:16 | Instagram Story, TikTok (1080 is not a multiple of 16) |
| 2160x3840 | 9:16 | 4K vertical poster |

### Social media

| Platform | Size | Notes |
|----------|-----------|---------|
| Instagram Post | 1080x1080 | Not a multiple of 16, use 1088x1088 |
| Instagram Story | 1080x1920 | Use 1088x1920 |
| Facebook Post | 1200x630 | Use 1200x640 (multiple of 16) |
| Twitter/X | 1200x675 | Use 1200x672 |
| LinkedIn | 1200x627 | Use 1200x624 |
| YouTube Thumbnail | 1280x720 | OK, already a multiple of 16 |

## Notes per mode

**Default path (`codex exec`)**: there is no size parameter. State the intended size inside the prompt, for example:
- "1024x1024 square format"
- "wide landscape 1536x1024"
- "tall portrait 1024x1536"

The model may not honor it exactly, but naming the ratio (square, wide, tall) steers the output.

**Fallback CLI (`scripts/image_gen.py`)**: exact control via `--size WxH` or `--size auto`. Total pixels above 2560x1440 are experimental. Details: `references/cli.md`.
