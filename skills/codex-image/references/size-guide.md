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
| 512x512 | 262K | Draft nhanh, preview |
| 1024x1024 | 1M | Icon, avatar, social post |
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
| 1080x1920 | 9:16 | Instagram Story, TikTok |

### Social Media

| Platform | Kích thước | Ghi chú |
|----------|-----------|---------|
| Instagram Post | 1080x1080 | Không chia hết cho 16, dùng 1088x1088 |
| Instagram Story | 1080x1920 | Dùng 1088x1920 |
| Facebook Post | 1200x630 | Dùng 1200x640 (chia hết cho 16) |
| Twitter/X | 1200x675 | Dùng 1200x672 |
| LinkedIn | 1200x627 | Dùng 1200x624 |
| YouTube Thumbnail | 1280x720 | OK, chia hết cho 16 |

## Lưu ý

Built-in tool không có tham số size. Ghi kích thước mong muốn trong prompt, ví dụ:
- "1024x1024 square format"
- "wide landscape 1792x1024"
- "tall portrait 1024x1792"

Model có thể không tuân thủ chính xác, nhưng mô tả tỷ lệ (square, wide, tall) giúp định hướng output.
