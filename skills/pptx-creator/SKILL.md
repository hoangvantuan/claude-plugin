---
name: pptx-creator
description: "Tạo PowerPoint (.pptx) đẹp, chuyên nghiệp bằng PptxGenJS (Node.js) — hỗ trợ font tiếng Việt (Be Vietnam Pro), design system (8 moods, 4 style recipes, color palettes), layout helpers chống overlap, series mode cho nhiều deck cùng bộ. Dùng khi user muốn 'tạo slide', 'làm PowerPoint', 'tạo presentation', 'tạo deck', 'làm bài trình bày', 'slide tiếng Việt', hoặc cần generate file .pptx từ code. Gồm 7-step workflow: requirements → palette/font → mood/style → outline → generate JS → compile → QA (visual + content). Khác skill pptx (đọc/sửa file có sẵn), skill này TẠO MỚI presentation từ đầu bằng code."
---

# PPTX Creator

Tạo presentation đẹp, chuyên nghiệp với hỗ trợ font tiếng Việt.

## Quick Reference

| Item            | Spec                                                          |
| --------------- | ------------------------------------------------------------- |
| Library         | PptxGenJS (Node.js)                                           |
| Layout          | LAYOUT_16x9 (10" x 5.625")                                   |
| Colors          | 6-char hex WITHOUT `#` — PptxGenJS sẽ lỗi nếu có `#`        |
| Default Font    | Be Vietnam Pro (body) + Montserrat (title)                    |
| Custom Font     | User có thể chỉ định font riêng qua `titleFont`/`bodyFont`   |
| Theme Keys      | `primary`, `secondary`, `accent`, `light`, `bg`, `titleFont`, `bodyFont` |
| Typography      | Title 36 → Heading 24 → Body 18 → Footnote 14 (tỷ lệ ~1.5x) |
| Page Badge      | x: 9.3", y: 5.1" (all slides except Cover)                   |

## Setup

```bash
# Required: PptxGenJS + icon stack
npm install -g pptxgenjs
npm install -g react-icons react react-dom sharp

# Required: text extraction QA (Step 7)
pip install "markitdown[pptx]"

# Required for Visual QA in Step 7 (Step 7 đánh dấu "Required")
# macOS:
brew install libreoffice poppler
# Ubuntu/Debian:
# apt install libreoffice poppler-utils
```

Cài `-g` global trên macOS/Linux có thể cần `sudo` nếu Node install vào `/usr/local`. Dùng `nvm` hoặc `volta` thay vì `sudo` được khuyến nghị.

**Vietnamese font (cần cài cả 2 chỗ):**

1. **Máy generate** (chạy compile.js): Download [Be Vietnam Pro](https://fonts.google.com/specimen/Be+Vietnam+Pro). PptxGenJS không embed font vào .pptx — chỉ ghi tên font.
2. **Máy presenter** (mở .pptx trình chiếu): cũng phải cài font Be Vietnam Pro. Nếu thiếu, PowerPoint fallback sang font hệ thống → dấu tiếng Việt vỡ.

Cài font:

```bash
# macOS (homebrew-cask-fonts)
brew tap homebrew/cask-fonts
brew install --cask font-be-vietnam-pro

# Linux: copy .ttf vào ~/.fonts/ rồi fc-cache -fv

# Windows: drag-drop .ttf vào Settings > Fonts
```

**Output location:** `slides/output/presentation.pptx` (sau khi chạy `node compile.js`). Open bằng PowerPoint, Keynote, hoặc LibreOffice.

---

## Workflow (7 Steps)

### Step 1: Understand Requirements

- Topic, audience, purpose, tone
- Number of slides (typical: 8-15)
- Content depth and key messages

### Step 2: Select Color Palette + Fonts

**Priority order:**

1. **Series mode** — Hỏi user upfront: "Đây là deck mới hay nằm trong series có sẵn?" Nếu series, check `series-config.json` ở project root (level cha của `slides/`). Nếu found, load và skip Steps 2-3. Chi tiết: [references/series-mode.md](references/series-mode.md)
2. **User custom** — nếu user cung cấp bộ màu hoặc font riêng, dùng trực tiếp.
3. **Catalog** — chọn từ bảng có sẵn trong [references/design-system.md](references/design-system.md).

```bash
# Auto-detect series (chạy trong project root, trước khi tạo slides/ subfolder)
ls series-config.json ../series-config.json 2>/dev/null
```

Nếu Claude đang ở project root (`my-presentation/`): check `./series-config.json`. Nếu đã `cd slides/`: check `../series-config.json`. Cả 2 path đều được compile.js auto-detect.

Custom palette: map hex codes vào 5 theme keys theo brightness (darkest → lightest). Custom font: gán `titleFont`/`bodyFont`, cảnh báo nếu không hỗ trợ Vietnamese. Chi tiết: [references/design-system.md](references/design-system.md#custom-color-palette).

### Step 3: Select Design Mood + Style

**3a. Design Mood** — xác định cảm xúc và tính cách. Read [references/design-system.md](references/design-system.md#design-moods):

- **Corporate Authority** — trang trọng, data-driven
- **Startup Energy** — táo bạo, aspirational
- **Editorial Elegance** — tinh tế, magazine-like
- **Playful Creative** — vui tươi, colorful
- **Minimal Zen** — tối giản cực đoan
- **Bold Brutalist** — mạnh mẽ, high-contrast
- **Warm Storytelling** — gần gũi, narrative
- **Data Dashboard** — analytical, structured

Mood guides every design decision: layout choice, density, visual elements, title style.

**3b. Style Recipe** — corner radius và spacing. Read [references/design-system.md](references/design-system.md#style-recipes):

- **Sharp** (0-0.05") — data-dense reports, corporate
- **Soft** (0.08-0.12") — balanced, professional (default)
- **Rounded** (0.15-0.25") — marketing, product
- **Pill** (0.3-0.5") — premium, brand

### Step 3.5: Generate Visual Assets (Nên làm khi có AI image tool)

Nếu có image generation tool, tạo assets nâng cao visual cho Cover/Summary slides. Read [references/design-system.md](references/design-system.md#background-techniques).

```bash
mkdir -p slides/assets
```

Prompt gợi ý: `"[Description], [color palette hex codes], 1920x1080, no text, no objects, suitable as presentation background"`

Save vào `slides/assets/`, reference trong slide code bằng `path: "./assets/filename.jpg"`.

### Step 3.7: Declare System & Confirm (BẮT BUỘC)

Trước khi plan outline, viết tóm tắt design system cho user xem rồi chờ confirm. Bước này tốn 30 giây nhưng tránh được kịch bản generate xong 12 slides mới biết user không thích mood.

Format declaration (5 dòng):

```
- Palette: <tên hoặc hex codes> (lý do chọn: <1 câu>)
- Mood: <tên mood> + Style Recipe: <Sharp/Soft/Rounded/Pill>
- Font: <titleFont> + <bodyFont>
- Số slide dự kiến: <N> (cover + toc + N-3 content + summary)
- Visual motif: <element lặp xuyên deck, ví dụ: pill badge, side border, icon circle>
```

Hỏi user: "Confirm system này hay muốn đổi gì?" Nếu user OK → tiếp Step 4. Nếu không → quay lại Step 2-3.

### Step 4: Plan Slide Outline

Classify EVERY slide as one of 5 types. Read [references/slide-types.md](references/slide-types.md):

1. **Cover** — Opening slide, dramatic title
2. **Table of Contents** — Navigation, 3-5 sections
3. **Section Divider** — Transition between sections
4. **Content** — Main content (9 subtypes: 4a-4i)
5. **Summary** — Closing, takeaways, CTA

Không lặp cùng layout trên slides liên tiếp, tạo visual variety. Bắt buộc điền **Outline Rhythm Table** (3 trục: tone, density, scale) ở [references/slide-types.md](references/slide-types.md#visual-rhythm-checklist-3-trục) trước khi sang Step 5. Đọc [anti-AI slop patterns](references/design-system.md#anti-ai-slop-patterns) song song.

### Step 5: Generate Slide JS Files

Create 1 JS file per slide in `slides/` directory. Each exports a synchronous `createSlide(pres, theme)` function.

Read [references/pptxgenjs-api.md](references/pptxgenjs-api.md) for API reference and critical pitfalls.

#### Step 5a: Showcase Checkpoint (BẮT BUỘC khi deck > 5 slides)

Đừng batch hết slides ngay. Trước tiên generate **2 slides showcase** đại diện cho design system:

1. **Cover slide** (định cảm giác mở deck).
2. **Slide content phức tạp nhất** trong outline (thường là 4d Big Stat, 4g Asymmetric Hero, hoặc 4h Staggered Cards).

Compile chỉ 2 slide này thành `showcase.pptx`, chạy Visual QA mini (Step 7 rút gọn: convert PDF, screenshot, check overlap + contrast + Vietnamese diacritics). Báo user: "Đây là 2 slide showcase, mood/palette/typography đã đúng ý chưa?"

Nếu user OK → generate phần còn lại (có thể song song subagents). Nếu không → fix system rồi mới batch. Tránh được kịch bản phải làm lại 13 lần thay vì 2 lần.

Skip checkpoint khi: deck ≤ 5 slides, hoặc đang dùng Series Mode (style đã chốt từ trước).

#### Layout Helper (dùng cho content slides — tránh overlap)

Import [scripts/layout-helpers.js](scripts/layout-helpers.js) để tính toán vị trí tự động:

```javascript
const { calcStack, calcColumns, calcGrid, estimateTextHeight, assertBounds,
        SAFE_AREA, TITLE_AREA, PAGE_BADGE } = require('../scripts/layout-helpers');
```

**Quy tắc:**

1. Không hardcode y positions cho stacked elements — dùng `calcStack(count, itemHeight)` (sẽ throw nếu vượt safe area)
2. Không hardcode column positions — dùng `calcColumns(count)` hoặc `calcGrid(cols, rows)`
3. Vietnamese text cao hơn ASCII ~30% — dùng `estimateTextHeight(lineCount, fontSize)`

**Layout Budget — max items per pattern:**

| Pattern | Max items | itemH | Gap | Total |
|---------|-----------|-------|-----|-------|
| Icon rows (4a) | 3-4 | 0.85" | 0.15" | 2.85" ✓ |
| Stat callouts (4d) | 3 | 1.1" | 0.2" | 3.7" ✓ |
| Staggered cards (4h) | 3 | 1.0" | 0.1" | 3.2" ✓ |
| TOC items | 5 | 0.65" | 0.1" | 3.65" ✓ |
| Columns (4b/4e) | 2-3 cols | full height | 0.2" gap | auto |

Kiểm tra trước khi code: `N × itemH + (N-1) × gap ≤ 3.8"` (SAFE_AREA.h). Nếu vượt → giảm N hoặc tách 2 slides.

#### Slide File Template

```javascript
const pptxgen = require("pptxgenjs");
const { calcStack, calcColumns, SAFE_AREA, TITLE_AREA, PAGE_BADGE } = require('../scripts/layout-helpers');

const slideConfig = {
  type: 'content',  // cover | toc | divider | content | summary
  index: 3,         // PHẢI khớp số trong filename slide-03.js → page badge hiện đúng
  title: 'Slide Title'
};

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  // -- YOUR SLIDE CONTENT HERE --
  // Title: fontSize 36, fontFace theme.titleFont, bold true
  // Body: fontSize 18-20, fontFace theme.bodyFont

  // Page badge (skip for cover)
  slide.addShape(pres.shapes.OVAL, {
    ...PAGE_BADGE, fill: { color: theme.accent }
  });
  slide.addText(String(slideConfig.index), {
    ...PAGE_BADGE,
    fontSize: 12, fontFace: theme.bodyFont,
    color: "FFFFFF", bold: true,
    align: "center", valign: "middle"
  });

  return slide;
}

// Standalone preview
if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  const theme = {
    primary: "264653", secondary: "2a9d8f",
    accent: "e9c46a", light: "f4a261", bg: "FAFAFA",
    titleFont: "Montserrat", bodyFont: "Be Vietnam Pro"
  };
  createSlide(pres, theme);
  pres.writeFile({ fileName: `slide-${String(slideConfig.index).padStart(2, '0')}-preview.pptx` });
}

module.exports = { createSlide, slideConfig };
```

Up to 5 slides can be generated concurrently via subagents. Each subagent receives the theme object and slide type specification.

### Step 6: Compile into Final PPTX

Copy [scripts/compile.js](scripts/compile.js) into `slides/` directory. Adjust `SLIDE_COUNT`, `pres.author`, `pres.title`, and `theme` object.

Run: `cd slides && node compile.js`

Output: `slides/output/presentation.pptx`. Compile.js in absolute path khi succeed + nhắc viewer apps trong console. Mở bằng PowerPoint, Keynote, hoặc LibreOffice.

**Boundary safety:** `calcStack` throw nếu vượt safe area. Slide hardcode positions nên gọi `assertBounds(elements)` cuối hàm `createSlide` — xem [scripts/layout-helpers.js](scripts/layout-helpers.js).

### Step 7: QA (Required)

Full checklist + commands: [references/qa-checklist.md](references/qa-checklist.md).

3 phần phải pass theo thứ tự:

1. **Content QA** — markitdown extract text, scan placeholder
2. **Visual QA** — convert PDF, screenshot per slide, check overlap/contrast/alignment
3. **Design Quality Review** — 5 câu test (Identity, Rhythm, Density, Mood, Hallmark)

Câu nào fail → fix → recompile → repeat full QA. Không deliver deck có ≥1 fail.

---

## Critical Rules (Summary)

Chi tiết + ví dụ cho mỗi rule: [references/design-system.md](references/design-system.md)

1. **Vietnamese diacritics** — text không dấu gây hiểu sai nghĩa và thiếu chuyên nghiệp. Luôn viết đầy đủ dấu, verify bằng markitdown sau compile.

2. **Hex colors không có `#`** — PptxGenJS corrupt file nếu có `#`. Dùng `"FF0000"` không phải `"#FF0000"`. Xem thêm: [references/pptxgenjs-api.md](references/pptxgenjs-api.md#critical-pitfalls)

3. **Không reuse option objects** — PptxGenJS mutates chúng. Tạo object mới mỗi lần.

4. **Body text tối thiểu 18pt** — 14-16pt quá nhỏ cho presentation. Chi tiết typography scale: [references/design-system.md](references/design-system.md#typography-scale)

5. **Vietnamese text cao hơn ASCII ~30%** — size text boxes generously, limit 4-5 bullets hoặc 3 content blocks/slide. Dùng `fit: true` khi text có thể tràn. Chi tiết: [references/design-system.md](references/design-system.md#vietnamese-text-overflow)

6. **Color contrast** — dark bg → white text (`"FFFFFF"`), light bg → dark text (`"222222"`). Check contrast của SHAPE fill, không phải slide bg. Chi tiết: [references/design-system.md](references/design-system.md#contrast-rules-critical)

7. **Visual element mỗi slide** — image, chart, icon, hoặc shape. Không để slide chỉ có text — thiếu visual hierarchy.

8. **Left-align body text** — center chỉ cho titles. Không dùng accent line dưới titles (dấu hiệu AI-generated).

---

## Series Mode

Khi tạo nhiều presentations cùng series (training Part 1, 2, 3), dùng `series-config.json` để giữ style nhất quán. Nếu phát hiện file này, load và skip Steps 2-3.

Chi tiết format, directory structure, ví dụ: [references/series-mode.md](references/series-mode.md)
