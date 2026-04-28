# Prompt Guide cho Codex Image Generation

## Cấu trúc prompt hiệu quả

```
[Subject] + [Medium/Style] + [Composition] + [Lighting] + [Color] + [Size] + [Details]
```

Không cần đủ tất cả thành phần. Thêm khi cần kiểm soát chi tiết hơn.

## Subject (Chủ thể)

Mô tả cụ thể, tránh mơ hồ.

| Kém        | Tốt                                                |
| ---------- | -------------------------------------------------- |
| a cat      | A fluffy orange tabby cat sitting on a windowsill  |
| a building | A brutalist concrete apartment building in Berlin  |
| food       | A bowl of Vietnamese pho with fresh herbs and lime |


## Medium / Style

| Style          | Mô tả trong prompt                                  |
| -------------- | --------------------------------------------------- |
| Ảnh thực       | photorealistic, DSLR photograph, 85mm lens          |
| Minh họa phẳng | flat design illustration, vector style, clean lines |
| Watercolor     | soft watercolor painting, wet-on-wet technique      |
| 3D render      | 3D rendered, Blender-style, smooth surfaces         |
| Pixel art      | pixel art, 16-bit style, retro gaming aesthetic     |
| Line art       | black and white line drawing, ink sketch            |
| Isometric      | isometric 3D view, game asset style                 |
| Oil painting   | oil painting on canvas, visible brushstrokes        |


## Composition

| Yêu cầu        | Prompt                                 |
| -------------- | -------------------------------------- |
| Centered       | centered composition, symmetrical      |
| Rule of thirds | off-center, rule of thirds placement   |
| Close-up       | extreme close-up, macro shot           |
| Wide shot      | wide angle, establishing shot          |
| Top-down       | top-down view, flat lay                |
| Isometric      | isometric perspective, 30-degree angle |


## Lighting

| Yêu cầu     | Prompt                                  |
| ----------- | --------------------------------------- |
| Tự nhiên    | natural daylight, soft diffused light   |
| Golden hour | warm golden hour sunlight, long shadows |
| Studio      | studio lighting, three-point setup      |
| Dramatic    | dramatic chiaroscuro, high contrast     |
| Neon        | neon glow, cyberpunk lighting           |
| Flat        | flat even lighting, no shadows          |


## Color Palette

Ghi rõ bảng màu mong muốn:

- "pastel color palette, soft pink and light blue"
- "monochrome, shades of gray"
- "vibrant saturated colors, tropical palette"
- "dark moody tones, deep navy and burgundy"
- "earth tones, warm browns and greens"

## Size (Kích thước)

Ghi trong prompt vì built-in tool không có tham số size.

| Use case          | Kích thước gợi ý | Prompt text                      |
| ----------------- | ---------------- | -------------------------------- |
| Icon / Avatar     | 1024x1024        | square format, 1024x1024         |
| Banner ngang      | 1792x1024        | wide landscape format, 1792x1024 |
| Story / Portrait  | 1024x1792        | tall portrait format, 1024x1792  |
| Social media post | 1080x1080        | square social media format       |
| Thumbnail         | 1280x720         | 16:9 thumbnail format            |


Lưu ý: model có thể không tuân thủ chính xác kích thước, nhưng mô tả tỷ lệ giúp định hướng.

## Text Rendering

gpt-image-2 render text chính xác hơn các model trước. Tips:

1. **Đặt text trong ngoặc kép**: `with the text "HELLO WORLD"`
2. **Ghi rõ font style**: `bold sans-serif`, `elegant serif`, `handwritten script`
3. **Vị trí**: `text centered at top`, `caption at bottom`
4. **Màu chữ**: `white text on dark background`, `black text`
5. **Kiểm tra chính tả**: model copy nguyên prompt, nên sai prompt sẽ sai text

**Ví dụ**: "A poster with the text 'OPEN MIC NIGHT' in bold retro font at the top, and 'Every Friday 8PM' in smaller italic text below, vintage microphone illustration in center, warm amber tones, 1024x1536"

## Transparent Background (Chroma-key)

Thêm vào cuối prompt:

- Nền xanh: `on a solid bright green (#00FF00) background, no shadows on background, crisp clean edges`
- Nền hồng (cho subject xanh): `on a solid magenta (#FF00FF) background, no shadows on background, crisp clean edges`

Sau đó dùng script `remove-chroma-key.py` để xóa nền.

## Anti-patterns (Tránh)

1. **Quá ngắn**: "a dog" (thiếu context, model tự quyết mọi thứ)
2. **Quá dài**: prompt >500 từ khiến model mất focus
3. **Mâu thuẫn**: "minimalist with lots of detail" (chọn 1)
4. **Negative prompt giả**: "no text, no watermark" (gpt-image-2 không hỗ trợ negative prompt mạnh, thay bằng mô tả cụ thể cái bạn MUỐN)
5. **Kích thước không hợp lệ**: cạnh phải chia hết cho 16, tỷ lệ tối đa 3:1
