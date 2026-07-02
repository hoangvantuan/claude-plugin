# QA Checklist (Step 7)

Load file này khi đến Step 7 của workflow. Skip Step 7 = ship deck với lỗi visual nhìn rõ ngay.

## Dependency Check

Visual QA cần `soffice` (LibreOffice) + `pdftoppm` (poppler):

```bash
# macOS
brew install libreoffice poppler

# Ubuntu/Debian
apt install libreoffice poppler-utils
```

Không cài được → fallback: open `.pptx` trong PowerPoint/Keynote, screenshot từng slide thủ công, check checklist bên dưới.

## Content QA

```bash
python -m markitdown output/presentation.pptx
python -m markitdown output/presentation.pptx | grep -iE "xxxx|lorem|ipsum|placeholder|TODO"
```

Bắt: text placeholder sót, encoding lỗi (mất dấu tiếng Việt thành "?"), bullet trùng.

## Visual QA (subagent với fresh eyes)

```bash
soffice --headless --convert-to pdf output/presentation.pptx --outdir output/
pdftoppm -jpeg -r 150 output/presentation.pdf output/slide
```

Subagent checklist:

- Overlapping elements (text đè shape, icon đè text)
- Low contrast (light text trên light bg, dark trên dark)
- Uneven gaps (icon rows lệch nhau, padding khác nhau)
- Insufficient margins (<0.5" từ mép slide)
- Misaligned columns (3 cards không cùng baseline)
- Placeholder content còn sót
- Font rendering issues (dấu tiếng Việt vỡ, fallback font system)

## Anti-AI Slop Check

Scan visual: repeated layouts, generic titles, missing visual variety. Reference: [design-system.md#anti-ai-slop-patterns](design-system.md#anti-ai-slop-patterns).

## Design Quality Review (5 câu test)

Visual QA bắt lỗi kỹ thuật. Design Quality Review bắt lỗi "đẹp nhưng generic". Sau khi pass Visual QA, tự trả lời 5 câu:

1. **Identity test**: Bỏ hết logo, page badge và text content. Slide còn nhận ra là deck của topic này không, hay có thể thuộc bất kỳ deck nào?
2. **Rhythm test**: Click xuyên 3 slide bất kỳ liên tiếp. Có cảm giác "mỗi slide một nhịp" không, hay tất cả cùng một layout?
3. **Density test**: Mỗi slide có đúng 1 core message không? Slide nào cần 2 câu để tóm tắt nội dung → tách 2 slides.
4. **Mood alignment test**: Slide có đang phản ánh mood đã chọn ở Step 3 không? Ví dụ chọn Minimal Zen mà slide có 5 decorative shapes là sai.
5. **Hallmark test**: Có accent line dưới title không? Có 3 icon cards đều nhau hàng ngang không? Có "Cảm ơn!" slide trống không? Bất kỳ "yes" nào → fix.

Câu nào fail → quay lại slide đó, fix. Không deliver deck có ≥1 fail.

## Verification Loop

Generate → Visual QA → Design Quality Review → Fix → Re-verify.

Fix xong rồi → recompile, repeat full QA. Đừng fix 1 slide rồi assume rest still pass.
