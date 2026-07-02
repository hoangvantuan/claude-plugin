# Size Guide cho gpt-image-2

## Ràng buộc kỹ thuật

- Cạnh tối đa: 3840 px
- Cả hai cạnh phải chia hết cho 16
- Tỷ lệ khung hình tối đa: 3:1
- Tổng pixel: 655,360 đến 8,294,400

## Kích thước thông dụng

### Square (1:1)

| Kích thước | Tổng pixel | Use case |
|-----------|------------|----------|
| 816x816 | 666K | Nhỏ nhất hợp lệ (draft nhanh — fallback CLI dùng `--quality low` thì nhanh hơn đổi size) |
| 1024x1024 | 1M | Icon, avatar, social post — nhanh nhất trong thực tế |
| 2048x2048 | 4.2M | In ấn chất lượng cao |

### Landscape (ngang)

| Kích thước | Tỷ lệ | Use case |
|-----------|--------|----------|
| 1536x1024 | 3:2 | Ảnh phong cảnh chuẩn |
| 1792x1024 | 7:4 | Banner website |
| 1920x1080 | 16:9 | Thumbnail YouTube, wallpaper |
| 2560x1440 | 16:9 | Wallpaper QHD |
| 3840x2160 | 16:9 | Wallpaper 4K |

### Portrait (dọc)

| Kích thước | Tỷ lệ | Use case |
|-----------|--------|----------|
| 1024x1536 | 2:3 | Story, poster dọc |
| 1024x1792 | 4:7 | Mobile wallpaper |
| 1088x1920 | ~9:16 | Instagram Story, TikTok (1080 không chia hết cho 16) |
| 2160x3840 | 9:16 | Poster dọc 4K |

### Social Media

| Platform | Kích thước | Ghi chú |
|----------|-----------|---------|
| Instagram Post | 1080x1080 | Không chia hết cho 16, dùng 1088x1088 |
| Instagram Story | 1080x1920 | Dùng 1088x1920 |
| Facebook Post | 1200x630 | Dùng 1200x640 (chia hết cho 16) |
| Twitter/X | 1200x675 | Dùng 1200x672 |
| LinkedIn | 1200x627 | Dùng 1200x624 |
| YouTube Thumbnail | 1280x720 | OK, chia hết cho 16 |

## Lưu ý theo mode

**Đường chính (`codex exec`)**: không có tham số size. Ghi kích thước mong muốn trong prompt, ví dụ:
- "1024x1024 square format"
- "wide landscape 1536x1024"
- "tall portrait 1024x1536"

Model có thể không tuân thủ chính xác, nhưng mô tả tỷ lệ (square, wide, tall) giúp định hướng output.

**Fallback CLI (`scripts/image_gen.py`)**: kiểm soát chính xác qua `--size WxH` hoặc `--size auto`. Trên 2560x1440 tổng pixel là experimental. Chi tiết: `references/cli.md`.
