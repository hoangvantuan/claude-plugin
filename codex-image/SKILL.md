---
name: codex-image
description: "Tạo và chỉnh sửa ảnh bitmap qua OpenAI Codex CLI (gpt-image-2), có fallback gọi thẳng OpenAI API. Hỗ trợ: text-to-image, nền trong suốt (chroma-key + native transparency gpt-image-1.5), batch generation, image editing (style transfer qua codex exec -i, edit chính xác/mask qua API), size chính xác tới 4K, quality control. Trigger: tạo ảnh, generate image, vẽ icon, logo, banner, illustration, minh họa, transparent background, xóa nền, ảnh trong suốt, batch ảnh, sửa ảnh, edit image, chỉnh ảnh, tạo ảnh hàng loạt, inpainting, ảnh 4K. KHÁC ai-artist (skill này dùng OpenAI gpt-image-2 trực tiếp + hỗ trợ edit ảnh có sẵn, ai-artist dùng Nano Banana với 129 curated prompts). KHÔNG dùng khi cần sửa SVG/vector/icon-system có sẵn trong repo hoặc đồ họa nên làm bằng HTML/CSS/SVG code-native."
argument-hint: "[mô tả ảnh] [--size WxH] [--transparent] [--batch N] [--edit input.png]"
---

# Codex Image: Tạo ảnh qua Codex CLI + OpenAI API fallback

Tạo và chỉnh sửa ảnh với model `gpt-image-2` (mặc định) qua hai chế độ.

## Hai chế độ

| Chế độ | Cơ chế | Điều kiện | Khi nào dùng |
|---|---|---|---|
| **Mặc định: `codex exec`** | Nhờ Codex agent gọi built-in tool `$imagegen` | Codex CLI + đăng nhập ChatGPT (không cần API key) | Mọi request thông thường: generate, biến tấu, chroma-key transparent, batch |
| **Fallback: `scripts/image_gen.py`** | Gọi thẳng OpenAI Image API | `OPENAI_API_KEY` + `openai`/`pillow` trong venv | Chỉ khi user yêu cầu rõ CLI/API/model control, HOẶC user xác nhận cần: size/quality chính xác, edit high-fidelity/mask, native transparency (gpt-image-1.5) |

Quy tắc chuyển chế độ:

- Không tự chuyển sang fallback chỉ vì cần chỉnh size/quality thông thường — hint trong prompt trước.
- **Không bao giờ âm thầm đổi xuống `gpt-image-1.5`** — đó là downgrade model, phải hỏi user trước (trừ khi user đã yêu cầu đích danh).
- Fallback cần `OPENAI_API_KEY`: nếu chưa có, hướng dẫn user tạo key tại https://platform.openai.com/api-keys và tự đặt env var — **không bao giờ yêu cầu user dán key vào chat**.
- **Không sửa `scripts/image_gen.py`** (script vendor từ OpenAI, Apache 2.0 — xem `scripts/LICENSE.txt`). Thiếu gì thì hỏi user.

## Khi nào KHÔNG dùng skill này

- Icon/logo/đồ họa UI cần khớp bộ SVG/vector **có sẵn trong repo** → sửa trực tiếp file vector.
- Hình khối đơn giản, diagram, wireframe → làm bằng SVG/HTML/CSS code-native tốt hơn.
- Ảnh đã tồn tại trong project ở định dạng editable, chỉ cần sửa nhỏ → sửa file gốc.

## Yêu cầu môi trường

```bash
codex --version   # Codex CLI: npm install -g @openai/codex, rồi chạy `codex` để login ChatGPT
```

Fallback CLI cần thêm: `uv pip install --python ~/.venv/claude/bin/python openai pillow` và `OPENAI_API_KEY`.

## Workflow

1. **Chế độ**: mặc định `codex exec`; fallback chỉ khi user yêu cầu rõ hoặc đã xác nhận.
2. **Ý định**: user muốn ảnh **mới** (kể cả có ảnh tham chiếu style/mood) → generate; muốn **giữ nguyên phần lớn ảnh cũ** → edit. Không rõ thì coi là generate.
3. **Số lượng**: 1 ảnh → 1 lệnh; nhiều asset khác nhau → mỗi asset 1 lệnh (hoặc `batch-generate.py`); nhiều prompt trên đường API → `generate-batch`.
4. **Prompt**: dựng theo schema bên dưới, áp dụng chính sách augmentation.
5. **Chạy → verify file tồn tại ở đích** (xem Chính sách output) → kiểm tra ảnh (subject, style, text, constraints) → iterate từng thay đổi một.
6. **Báo cáo**: path cuối cùng, prompt đã dùng, chế độ nào.

## 1. Text-to-Image (đường chính)

```bash
codex exec --skip-git-repo-check --enable image_generation \
  '$imagegen <PROMPT>. Save the final PNG as <TÊN_FILE>.png in <THƯ_MỤC_OUTPUT_TUYỆT_ĐỐI>.'
```

- Built-in tool chỉ nhận prompt text: size, style, quality đều mô tả trong prompt ("1024x1024 square format", "wide landscape 1536x1024"). Chọn size: `references/size-guide.md`.
- Ví dụ: `'$imagegen A minimal flat-design coffee cup icon, white background, 1024x1024. Save as coffee-icon.png in /path/to/output.'`

## 2. Nền trong suốt (transparent)

Mặc định dùng chroma-key trên đường chính (gpt-image-2 không hỗ trợ `background=transparent`):

**Bước 1 — Generate trên nền chroma-key.** Thêm vào prompt (nguyên văn):

```text
Create the requested subject on a perfectly flat solid #00ff00 chroma-key background for background removal.
The background must be one uniform color with no shadows, gradients, texture, reflections, floor plane, or lighting variation.
Keep the subject fully separated from the background with crisp edges and generous padding.
Do not use #00ff00 anywhere in the subject.
No cast shadow, no contact shadow, no reflection, no watermark, and no text unless explicitly requested.
```

Subject có màu xanh lá → thay bằng `#ff00ff` (magenta). Tránh key màu trùng subject.

**Bước 2 — Xóa nền cục bộ:**

```bash
~/.venv/claude/bin/python skills/codex-image/scripts/remove_chroma_key.py \
  --input <source.png> --out <final.png> \
  --auto-key border --soft-matte \
  --transparent-threshold 12 --opaque-threshold 220 --despill
```

Lưu ý `--despill`: khử ánh xanh lây ở cạnh, nhưng **tẩy luôn màu xanh thật trong subject** (đã kiểm chứng: lá táo xanh bị biến thành xám). Subject có phần màu gần key → bỏ `--despill`, hoặc tốt hơn là dùng key magenta ngay từ bước 1.

**Bước 3 — Validate**: mở ảnh ra nhìn — output phải có alpha channel, 4 góc trong suốt, subject coverage hợp lý, không viền màu key, **màu subject không bị biến đổi**. Còn viền mảnh → retry một lần thêm `--edge-contract 1`; cạnh răng cưa rõ (subject không bóng/phản chiếu) → thêm `--edge-feather 0.25`.

**Đường thoát — native transparency.** Nếu user cần transparency thật, subject phức tạp (tóc, lông, khói, thủy tinh, chất lỏng, vật phản chiếu, bóng mềm), hoặc chroma-key fail validation → giải thích và **hỏi user trước** khi chạy fallback:

```bash
~/.venv/claude/bin/python skills/codex-image/scripts/image_gen.py generate \
  --model gpt-image-1.5 --prompt "<PROMPT>" \
  --background transparent --output-format png --out <final.png>
```

(Cần `OPENAI_API_KEY`; chưa có thì hướng dẫn đặt key. Phương án chót không cần key: tool chuyên dụng như remove.bg/Photoshop.)

## 3. Batch (nhiều ảnh)

**Đường chính** — script gọi `codex exec` tuần tự cho từng prompt, tự đặt tên `prefix-001.png`...:

```bash
~/.venv/claude/bin/python skills/codex-image/scripts/batch-generate.py \
  --prompts "prompt 1" "prompt 2" --output-dir ./output-images/ --prefix batch
# hoặc --prompt-file prompts.txt (mỗi dòng 1 prompt)
```

**Đường API** (chỉ khi user đã chọn fallback) — chạy song song từ JSONL, xem `references/cli.md`:

```bash
~/.venv/claude/bin/python skills/codex-image/scripts/image_gen.py generate-batch \
  --input prompts.jsonl --out-dir output/ --concurrency 5
```

Lưu ý: chữ "batch" trong request KHÔNG có nghĩa là chuyển sang API fallback. Nhiều asset khác nhau = nhiều prompt riêng, không dùng `--n` (n chỉ dành cho biến thể của cùng 1 prompt).

## 4. Image Editing

Phân luồng theo mức bảo toàn ảnh gốc:

| Yêu cầu | Đường | Cơ chế |
|---|---|---|
| Biến tấu, style transfer, "vẽ lại theo hướng..." | `codex exec -i` (mặc định) | Model nhìn ảnh → tả lại → generate mới. Composition giữ khá tốt, KHÔNG phải edit pixel-level |
| Bảo toàn chính xác: giữ mặt/người, xóa/thay 1 vật thể, đổi nền giữ subject, sửa text trong ảnh, mask/inpainting | `image_gen.py edit` (fallback, hỏi trước) | Ảnh đưa thẳng vào edit endpoint; gpt-image-2 luôn high-fidelity; hỗ trợ `--mask` |

**Đường chính** (lưu ý: phải có `exec` và dấu `--` ngăn flag `-i` nuốt prompt):

```bash
codex exec --skip-git-repo-check --enable image_generation \
  -i <ảnh_gốc.png> -- '$imagegen Modify this image: <MÔ_TẢ>. Change only X; keep Y unchanged. Save as <output>.png in <thư_mục>.'
```

Nhiều ảnh tham chiếu: `-i style-ref.png,content-ref.png` — trong prompt gọi ảnh theo index và vai trò (Image 1: style reference...).

**Đường API:**

```bash
~/.venv/claude/bin/python skills/codex-image/scripts/image_gen.py edit \
  --image input.png --prompt "Replace only the background with a warm sunset; keep the subject unchanged" \
  --out edited.png
```

Quy tắc invariants: mọi prompt edit phải ghi rõ `change only X; keep Y unchanged`, và **lặp lại ở mỗi vòng iterate** để chống drift.

## 5. Prompt

Schema (dùng các dòng cần thiết, không phải điền đủ):

```text
Use case: <slug taxonomy>
Primary request: <yêu cầu chính của user>
Subject / Scene: <chủ thể + bối cảnh>
Style/medium: <photo/illustration/3D...>
Composition/framing: <wide/close/top-down; placement>
Lighting/mood: <ánh sáng + mood>
Text (verbatim): "<text chính xác>"
Constraints: <phải giữ / phải tránh>
```

Chính sách augmentation:

- Prompt user **đã chi tiết** → chỉ chuẩn hóa thành spec sạch, KHÔNG thêm yêu cầu sáng tạo.
- Prompt **chung chung** → được thêm chi tiết có chừng mực (composition, mức polish, bối cảnh hợp lý). KHÔNG thêm nhân vật/vật thể/brand/slogan không được ngụ ý.
- Thiếu chi tiết then chốt chặn thành công → hỏi user; còn lại cứ tiến hành.

Taxonomy use-case (slug): generate — `photorealistic-natural`, `product-mockup`, `ui-mockup`, `infographic-diagram`, `scientific-educational`, `ads-marketing`, `productivity-visual`, `logo-brand`, `illustration-story`, `stylized-concept`, `historical-scene`; edit — `text-localization`, `identity-preserve`, `precise-object-edit`, `lighting-weather`, `background-extraction`, `style-transfer`, `compositing`, `sketch-to-render`.

Chi tiết nguyên tắc: `references/prompting.md`. Recipe copy/paste theo use-case: `references/sample-prompts.md`.

## Chính sách output

1. Prompt luôn chỉ rõ "Save as X.png in <thư mục tuyệt đối>". Sau khi `codex exec` xong, **verify file tồn tại ở đích**; không thấy → tìm ảnh mới nhất trong `~/.codex/generated_images/` copy về đích rồi báo user.
2. **Không bao giờ để asset của project nằm lại chỉ ở `~/.codex/generated_images/`**.
3. **Không ghi đè file có sẵn** trừ khi user yêu cầu rõ — tạo tên phiên bản (`hero-v2.png`, `icon-edited.png`).
4. Kết thúc luôn báo: path cuối cùng, prompt đã dùng, chế độ nào.

## Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân | Giải pháp |
|---|---|---|
| `codex: command not found` | Chưa cài Codex CLI | `npm install -g @openai/codex` |
| `image_generation is not enabled` | Feature chưa bật | Thêm `--enable image_generation` |
| `Authentication required` | Chưa đăng nhập | Chạy `codex` và đăng nhập ChatGPT |
| `No prompt provided via stdin` | Flag `-i` nuốt prompt | Thêm `--` trước prompt: `-i img.png -- '$imagegen ...'` |
| Mở TUI thay vì chạy | Thiếu `exec` | Dùng `codex exec ...` |
| File không xuất hiện ở đích | Codex lưu vào default path | Tìm trong `~/.codex/generated_images/`, copy về đích |
| Ảnh sai kích thước (đường chính) | Model tự quyết | Ghi rõ size trong prompt; cần chính xác tuyệt đối → fallback `--size` |
| Text sai chính tả trong ảnh | Prompt chưa rõ | Text trong ngoặc kép, spell letter-by-letter từ khó |
| Viền xanh sau xóa nền | Cạnh mờ/antialiasing | Retry `--edge-contract 1`; phức tạp quá → hỏi fallback gpt-image-1.5 |
| Màu xanh trong subject bị xám hóa | `--despill` tẩy nhầm màu thật | Chạy lại không có `--despill`, hoặc generate lại trên nền magenta |
| `OPENAI_API_KEY` missing (fallback) | Chưa đặt key | Hướng dẫn tạo key + đặt env var, không dán key vào chat |

## Reference map

- `references/prompting.md` — nguyên tắc prompt (2 chế độ dùng chung) + bảng từ vựng style/composition/lighting
- `references/sample-prompts.md` — recipe copy/paste theo use-case (2 chế độ dùng chung)
- `references/size-guide.md` — chọn kích thước theo use case + constraint gpt-image-2
- `references/cli.md` — fallback CLI: lệnh, flags, quality, mask, batch JSONL (chỉ đọc khi vào fallback)
- `references/image-api.md` — tham số Image API (chỉ đọc khi vào fallback)
- `scripts/image_gen.py` — fallback CLI (vendor từ OpenAI Codex, Apache 2.0, không sửa)
- `scripts/remove_chroma_key.py` — xóa nền chroma-key (vendor từ OpenAI Codex, Apache 2.0)
- `scripts/batch-generate.py` — batch tuần tự trên đường `codex exec`
- `scripts/LICENSE.txt` — Apache License 2.0 cho các script vendor
