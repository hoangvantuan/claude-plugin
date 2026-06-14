---
name: codex-image
description: "Tạo và chỉnh sửa ảnh bằng OpenAI Codex CLI (gpt-image-2). Hỗ trợ: text-to-image, nền trong suốt (chroma-key), batch generation nhiều ảnh, image editing (style transfer, chỉnh sửa theo mô tả). Trigger: tạo ảnh, generate image, vẽ icon, logo, banner, illustration, minh họa, transparent background, xóa nền, ảnh trong suốt, batch ảnh, sửa ảnh, edit image, chỉnh ảnh, tạo ảnh hàng loạt. KHÁC ai-artist (skill này dùng OpenAI gpt-image-2 trực tiếp + hỗ trợ edit ảnh có sẵn, ai-artist dùng Nano Banana với 129 curated prompts)."
argument-hint: "[mô tả ảnh] [--size WxH] [--transparent] [--batch N] [--edit input.png]"
---

# Codex Image: Tạo ảnh qua Codex CLI

Tạo và chỉnh sửa ảnh bằng OpenAI Codex CLI với model `gpt-image-2`.

## Yêu cầu

- **Codex CLI** đã cài: `npm install -g @openai/codex`
- Đã đăng nhập ChatGPT hoặc đặt `OPENAI_API_KEY`
- Feature `image_generation` bật (mặc định từ v0.124.0)

Kiểm tra nhanh:

```bash
codex --version
```

Nếu chưa cài, hướng dẫn user cài trước khi tiếp tục.

## Workflow tổng quan

```
User mô tả ảnh → Craft prompt tối ưu → codex exec → Lưu file → Post-process (nếu cần)
```

## 1. Tạo ảnh cơ bản (Text-to-Image)

### Lệnh chuẩn

```bash
codex exec --skip-git-repo-check --enable image_generation \
  '$imagegen <PROMPT_MÔ_TẢ_ẢNH>. Save the final PNG as <TÊN_FILE>.png in <THƯ_MỤC_OUTPUT>.'
```

### Ví dụ

```bash
# Icon đơn giản
codex exec --skip-git-repo-check --enable image_generation \
  '$imagegen A minimal flat-design coffee cup icon, white background, 1024x1024. Save as coffee-icon.png in current directory.'

# Banner phong cảnh
codex exec --skip-git-repo-check --enable image_generation \
  '$imagegen A panoramic watercolor landscape of Mount Fuji at sunset, wide format 1792x1024. Save as fuji-banner.png in current directory.'

# Logo chữ
codex exec --skip-git-repo-check --enable image_generation \
  '$imagegen A modern minimalist logo with the text "HELLO" in bold geometric sans-serif, dark navy on white, 1024x1024. Save as hello-logo.png in current directory.'
```

### Kiểm soát output qua prompt

Built-in `image_gen` tool chỉ nhận tham số `prompt`. Mọi yêu cầu về kích thước, phong cách, chất lượng phải mô tả trong prompt.

**Kích thước**: Ghi rõ trong prompt. Ví dụ: "1024x1024 square format", "wide 1792x1024 landscape", "tall 1024x1792 portrait". Xem `references/size-guide.md` để chọn kích thước phù hợp.

**Phong cách**: Mô tả cụ thể style mong muốn. Ví dụ: "flat design", "watercolor", "photorealistic", "minimalist line art", "3D render".

**Chất lượng text**: gpt-image-2 render text tốt. Ghi rõ nội dung text và font style trong prompt.

## 2. Transparent Background (Nền trong suốt)

Built-in tool không hỗ trợ transparent trực tiếp. Dùng quy trình chroma-key:

### Bước 1: Tạo ảnh trên nền chroma-key

```bash
codex exec --skip-git-repo-check --enable image_generation \
  '$imagegen <MÔ_TẢ_SUBJECT> on a solid bright green (#00FF00) background, no shadows on background, crisp edges. Save as raw-<TÊN>.png in current directory.'
```

Nếu subject có màu xanh lá, dùng nền magenta `#FF00FF` thay thế.

### Bước 2: Xóa nền chroma-key

```bash
~/.venv/claude/bin/python skills/codex-image/scripts/remove-chroma-key.py \
  raw-<TÊN>.png \
  -o <TÊN>.png \
  --color green
```

Script hỗ trợ `--color green` (mặc định) hoặc `--color magenta`. Kết quả là PNG với alpha channel.

### Lưu ý subject phức tạp

Với subject có cạnh mờ (tóc, lông, khói, thủy tinh): chroma-key có thể để lại viền xanh. Trong trường hợp này:

- Tăng `--tolerance` (mặc định 30, thử 40-50)
- Hoặc gợi ý user dùng tool chuyên dụng (remove.bg, Photoshop)

## 3. Batch Generation (Tạo nhiều ảnh)

Dùng script batch để tạo nhiều ảnh từ danh sách prompt:

### Cách 1: Danh sách prompt inline

```bash
~/.venv/claude/bin/python skills/codex-image/scripts/batch-generate.py \
  --prompts "prompt 1" "prompt 2" "prompt 3" \
  --output-dir ./output-images/ \
  --prefix "batch"
```

### Cách 2: File prompt (mỗi dòng 1 prompt)

```bash
~/.venv/claude/bin/python skills/codex-image/scripts/batch-generate.py \
  --prompt-file prompts.txt \
  --output-dir ./output-images/ \
  --prefix "series"
```

Script gọi `codex exec` cho từng prompt, đặt tên file tự động: `batch-001.png`, `batch-002.png`, ...

## 4. Image Editing (Chỉnh sửa ảnh)

### Chế độ interactive

Codex CLI hỗ trợ đưa ảnh tham chiếu vào context:

```bash
codex -i <ảnh_gốc.png> \
  '$imagegen Modify this image: <MÔ_TẢ_THAY_ĐỔI>. Save as edited-output.png in current directory.'
```

Nhiều ảnh tham chiếu:

```bash
codex -i style-ref.png,content-ref.png \
  '$imagegen Combine the style of the first image with the content of the second. Save as combined.png in current directory.'
```

### Hạn chế

- Flag `-i` đưa ảnh vào context để model "nhìn", nhưng built-in `image_gen` tool KHÔNG nhận ảnh input trực tiếp
- Model sẽ mô tả lại ảnh trong prompt khi gọi tool, nên kết quả là "lấy cảm hứng" chứ không phải edit pixel-level
- Với inpainting chính xác (mask-based), cần dùng OpenAI API trực tiếp

## 5. Craft Prompt hiệu quả

Xem chi tiết tại `references/prompt-guide.md`. Tóm tắt:

### Cấu trúc prompt tốt

```
[Subject chính] + [Style/Medium] + [Composition] + [Lighting] + [Color palette] + [Kích thước] + [Chi tiết bổ sung]
```

### Ví dụ prompt tốt vs. kém

**Kém**: "a cat"

**Tốt**: "A fluffy orange tabby cat sitting on a windowsill, soft watercolor illustration style, warm afternoon sunlight streaming in, pastel color palette, 1024x1024 square format, detailed fur texture"

### Prompt cho text rendering

gpt-image-2 render chữ chính xác. Ghi rõ:

- Nội dung text chính xác (đặt trong ngoặc kép nếu cần)
- Font style: serif, sans-serif, handwritten, bold, italic
- Vị trí text: center, top, bottom
- Kích thước tương đối: large heading, small caption

## Xử lý lỗi thường gặp

| Lỗi                               | Nguyên nhân               | Giải pháp                                                |
| --------------------------------- | ------------------------- | -------------------------------------------------------- |
| `codex: command not found`        | Chưa cài Codex CLI        | `npm install -g @openai/codex`                           |
| `image_generation is not enabled` | Feature chưa bật          | Thêm flag `--enable image_generation`                    |
| `Authentication required`         | Chưa đăng nhập            | Chạy `codex` và đăng nhập ChatGPT                        |
| Ảnh không đúng kích thước         | Model tự quyết kích thước | Ghi rõ kích thước trong prompt, ví dụ "1024x1024 square" |
| Text sai chính tả trong ảnh       | Prompt chưa rõ            | Đặt text trong ngoặc kép, ghi rõ spelling                |
| Timeout                           | Prompt phức tạp           | Chia nhỏ prompt, giảm chi tiết                           |


## Output mặc định

- Built-in tool lưu ảnh tại: `~/.codex/generated_images/`
- Prompt nên chỉ rõ "Save as X.png in current directory" để Codex copy ảnh ra thư mục làm việc
- Format: PNG (mặc định)
