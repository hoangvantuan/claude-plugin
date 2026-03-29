---
name: pptx-creator
description: "Create beautiful, professional PowerPoint presentations with Vietnamese font support and modern design. Use this skill any time a .pptx file needs to be created from scratch — slide decks, pitch decks, training materials, business presentations, or any PowerPoint creation task. Triggers on: PPTX, PowerPoint, presentation, slide deck, slides, tao slide, tao bai thuyet trinh, lam PowerPoint. This skill focuses on CREATING new presentations from scratch using PptxGenJS with a built-in design system optimized for Vietnamese content. For editing existing .pptx files, use the standard pptx skill instead."
---

# PPTX Creator

Tạo presentation đẹp, chuyên nghiệp với hỗ trợ font tiếng Việt.

## Quick Reference

| Item            | Spec                                                          |
| --------------- | ------------------------------------------------------------- |
| Library         | PptxGenJS (Node.js)                                           |
| Layout          | LAYOUT_16x9 (10" x 5.625")                                   |
| Colors          | 6-char hex WITHOUT `#`                                        |
| Default Font    | Be Vietnam Pro (body) + Montserrat (title)                    |
| Custom Font     | User có thể chỉ định font riêng qua `titleFont`/`bodyFont`   |
| Theme Keys      | `primary`, `secondary`, `accent`, `light`, `bg`, `titleFont`, `bodyFont` |
| Typography      | Title 36 → Heading 24 → Body 18 → Footnote 14                |
| Page Badge      | x: 9.3", y: 5.1" (all slides except Cover)                   |


## Setup

```bash
npm install -g pptxgenjs
npm install -g react-icons react react-dom sharp  # for icons
pip install "markitdown[pptx]"                     # for QA text extraction
```

**Vietnamese font**: Download [Be Vietnam Pro](https://fonts.google.com/specimen/Be+Vietnam+Pro) and install on your system. This font has excellent Vietnamese diacritic support and looks professional.

---

## Workflow (7 Steps)

### Step 1: Understand Requirements

- Topic, audience, purpose, tone
- Number of slides (typical: 8-15)
- Content depth and key messages

### Step 2: Select Color Palette + Fonts

**Priority order:**

1. **Series mode** — check `series-config.json` in working/parent directory. If found, load and skip Steps 2-3.
2. **User custom** — nếu user cung cấp bộ màu hoặc font riêng, dùng trực tiếp (xem bên dưới).
3. **Catalog** — chọn từ bảng có sẵn trong [references/design-system.md](references/design-system.md).

```bash
# Auto-detect series
ls series-config.json ../series-config.json 2>/dev/null
```

**Custom palette từ user:** Khi user cung cấp bộ màu (hex codes), map vào 5 theme keys theo brightness (darkest → lightest). Xem chi tiết: [references/design-system.md](references/design-system.md#custom-color-palette).

**Custom font từ user:** Khi user chỉ định font, gán vào `titleFont`/`bodyFont` trong theme object. Cảnh báo nếu font không hỗ trợ Vietnamese. Xem chi tiết: [references/design-system.md](references/design-system.md#custom-font).

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

### Step 3.5: Generate Visual Assets (Optional but Recommended)

Dùng `ai-multimodal` skill tạo assets nâng cao visual. Read [references/design-system.md](references/design-system.md#background-techniques):

1. **Background images** — gradient, texture, pattern cho Cover/Summary slides
2. **Hero images** — illustrations, photos cho Content slides
3. **Custom decorative elements** — shapes, patterns matching the mood

```bash
# Tạo assets directory
mkdir -p slides/assets
```

Prompt template cho `ai-multimodal`:
```
"[Description], [color palette hex codes], 1920x1080, no text, no objects, suitable as presentation background"
```

Save vào `slides/assets/`, reference trong slide code bằng `path: "./assets/filename.jpg"`.

### Step 4: Plan Slide Outline

Classify EVERY slide as one of 5 types. Read [references/slide-types.md](references/slide-types.md):

1. **Cover** — Opening slide, dramatic title
2. **Table of Contents** — Navigation, 3-5 sections
3. **Section Divider** — Transition between sections
4. **Content** — Main content (9 subtypes: 4a-4i)
5. **Summary** — Closing, takeaways, CTA

**Enforce visual variety** — never repeat the same layout on consecutive slides.
**Anti-AI Slop** — read [references/design-system.md](references/design-system.md#anti-ai-slop-patterns) before finalizing outline.

### Step 5: Generate Slide JS Files

Create 1 JS file per slide in `slides/` directory. Each exports a synchronous `createSlide(pres, theme)` function.

Read [references/pptxgenjs-api.md](references/pptxgenjs-api.md) for the complete API reference and critical pitfalls to avoid.

**Slide file template:**

```javascript
const pptxgen = require("pptxgenjs");

const slideConfig = {
  type: 'content',  // cover | toc | divider | content | summary
  index: 3,
  title: 'Slide Title'
};

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  // -- YOUR SLIDE CONTENT HERE --
  // Title: fontSize: 36, fontFace: theme.titleFont, bold: true
  // Heading: fontSize: 24, fontFace: theme.titleFont, bold: true
  // Body: fontSize: 18-20, fontFace: theme.bodyFont
  // Footnote: fontSize: 14, fontFace: theme.bodyFont

  // Page badge (required for all except cover)
  slide.addShape(pres.shapes.OVAL, {
    x: 9.3, y: 5.1, w: 0.4, h: 0.4,
    fill: { color: theme.accent }
  });
  slide.addText(String(slideConfig.index), {
    x: 9.3, y: 5.1, w: 0.4, h: 0.4,
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

**Use subagents**: Up to 5 slides can be generated concurrently via subagents. Each subagent receives the theme object and slide type specification.

### Step 6: Compile into Final PPTX

Copy [scripts/compile.js](scripts/compile.js) into your `slides/` directory. Adjust `SLIDE_COUNT`, `pres.author`, `pres.title`, and `theme` object to match your presentation.

Run: `cd slides && node compile.js`

### Step 7: QA (Required)

**Content QA:**

```bash
python -m markitdown output/presentation.pptx
python -m markitdown output/presentation.pptx | grep -iE "xxxx|lorem|ipsum|placeholder|TODO"
```

**Visual QA** (use subagent with fresh eyes):

```bash
# Convert to images for visual inspection (requires LibreOffice + poppler)
soffice --headless --convert-to pdf output/presentation.pptx --outdir output/
pdftoppm -jpeg -r 150 output/presentation.pdf output/slide
```

Give the subagent this checklist:

- Overlapping elements or text overflow
- Low contrast (light on light / dark on dark)
- Uneven gaps or cramped sections
- Insufficient margins (< 0.5")
- Misaligned columns or cards
- Leftover placeholder content
- Font rendering issues with Vietnamese diacritics

**AI Visual QA** (recommended — dùng `ai-multimodal` skill):

Sau khi convert slides thành images, dùng `ai-multimodal` để phân tích:

```
Prompt cho ai-multimodal:
"Analyze this presentation slide image. Check for:
1. Text readability — any low contrast text?
2. Layout balance — any cramped or empty areas?
3. Visual hierarchy — is the most important element prominent?
4. Consistency — does this match a professional design standard?
5. AI-generated patterns — accent lines under titles, identical card layouts, generic visuals?
Rate overall quality 1-10 and list specific fixes needed."
```

**Anti-AI Slop Check** (self-review toàn deck):

1. Scan all slide layouts — có lặp pattern không?
2. Check titles — generic hay specific?
3. Verify visual variety — mỗi slide có visual element khác nhau?
4. Read [references/design-system.md](references/design-system.md#anti-ai-slop-patterns) và đối chiếu

**Verification loop**: Generate -> Inspect -> Fix -> Re-verify. Don't declare success after one pass.

---

## Critical Rules

### Vietnamese Content (CRITICAL)

ALL Vietnamese text MUST have proper diacritics (dấu). This is non-negotiable — Vietnamese without diacritics is unreadable and unprofessional.

```
WRONG: "Ung dung suc khoe so 1 Viet Nam"
RIGHT: "Ứng dụng sức khỏe số 1 Việt Nam"

WRONG: "Nguoi dung"     RIGHT: "Người dùng"
WRONG: "Giai phap"      RIGHT: "Giải pháp"
WRONG: "Cong nghe"      RIGHT: "Công nghệ"
```

After generating the PPTX, run markitdown to verify — if ANY Vietnamese text appears without diacritics, fix it immediately.

### Vietnamese Font Support

- **Default**: `Be Vietnam Pro` (body) + `Montserrat` (title). Fallback: `Arial`.
- **Custom font**: Gán qua `titleFont`/`bodyFont` trong theme object.
- Danh sách font an toàn cho tiếng Việt + font pairings: [references/design-system.md](references/design-system.md#font-reference)

### Theme Object Contract

7 keys bắt buộc: 5 colors (`primary`, `secondary`, `accent`, `light`, `bg`) + 2 fonts (`titleFont`, `bodyFont`).

- Color: Hex 6 ký tự, KHÔNG có `#`. `titleFont` → title + heading. `bodyFont` → body, bullets, captions, badge.
- Default: `titleFont: "Montserrat"`, `bodyFont: "Be Vietnam Pro"`.
- Chi tiết + code example: [references/design-system.md](references/design-system.md#theme-object)

### File Corruption Prevention

Read [references/pptxgenjs-api.md](references/pptxgenjs-api.md#critical-pitfalls) for the full list. The top 3:

1. **NO `#` in hex colors** — `"FF0000"` not `"#FF0000"`
2. **NO 8-char hex** — use `opacity` property instead
3. **NO reusing option objects** — PptxGenJS mutates them. Create fresh each time.

### Font Size (Important — Text Must Be Readable)

Typography: **Title 36 → Heading 24 → Body 18 → Footnote 14** (tỷ lệ ~1.5x). Cover slide cho phép title 44-60pt.

Chi tiết đầy đủ: [references/design-system.md](references/design-system.md#typography-scale)

**Lưu ý:** Body text 14-16pt quá nhỏ cho presentation. Luôn dùng 18pt+ cho text người xem cần đọc.

### Preventing Text Overflow (Important for Vietnamese)

Vietnamese with diacritics (ă, ệ, ồ, ử, ớ) is taller and wider than ASCII text. Combined with larger font sizes, text will overflow boxes if you're not careful.

**Rules to prevent overflow:**

1. **Size text boxes generously** — add 30% extra height vs what you'd use for English. A 2-line Vietnamese title at 44pt needs ~1.4" height (not 1.0").

2. **Limit content per slide** — with 18-20pt body text, fit max 4-5 bullet points or 3 content blocks per slide. If content is long, split across 2 slides.

3. **Use `fit: true` for auto-shrink** when text might overflow:
   ```javascript
   slide.addText("Tiêu đề có thể dài", {
     x: 0.5, y: 0.5, w: 9, h: 1.2,
     fontSize: 44, fontFace: "Be Vietnam Pro",
     fit: true  // auto-shrink if text overflows
   });
   ```

4. **Text box height guidelines for Vietnamese:**
   | Font Size | 1 line | 2 lines | 3 lines |
   |-----------|--------|---------|---------|
   | 36pt title | 0.7" | 1.3" | 1.9" |
   | 24pt heading | 0.5" | 0.95" | 1.4" |
   | 20pt body | 0.45" | 0.8" | 1.15" |
   | 14pt footnote | 0.35" | 0.6" | 0.85" |

5. **Keep text concise** — Vietnamese descriptions should be 1-2 sentences max per block. Don't cram long paragraphs into slides.

6. **Test before finalizing** — always run markitdown + visual QA to catch overflow.

### Color Contrast (CRITICAL — Text Must Be Readable)

Dark bg → white text (`"FFFFFF"`). Light bg → dark text (`"222222"` hoặc `theme.primary`). Luôn check contrast của SHAPE fill, không phải slide bg.

Safe colors, DO/DON'T examples, validation checklist: [references/design-system.md](references/design-system.md#contrast-rules-critical)

### Design Principles

- **Every slide needs a visual element** — image, chart, icon, or shape. No text-only slides.
- **Left-align body text** — center only titles
- **NEVER use accent lines under titles** — hallmark of AI-generated slides
- **Vary layouts** — don't repeat the same layout consecutively
- **60-70% primary color dominance** — 1-2 supporting, 1 sharp accent
- **0.5" minimum margins**, 0.3-0.5" between content blocks
- **Follow chosen Design Mood** — mỗi quyết định design phải consistent với mood đã chọn
- **Avoid AI Slop** — read [references/design-system.md](references/design-system.md#anti-ai-slop-patterns) for patterns to avoid
- **Use background images** cho Cover/Summary slides thay vì solid colors khi có thể

---

## Series Mode (Multiple Presentations, Same Style)

When creating multiple presentations in a series (e.g., training Part 1, 2, 3), save the style config once and reuse it across all decks.

### Step 1: Create `series-config.json` for the first presentation

```json
{
  "series": "Kỹ Năng Mềm Training 2026",
  "mood": "Warm Storytelling",
  "theme": {
    "primary": "1B2A4A",
    "secondary": "2E4A7A",
    "accent": "6B8FBF",
    "light": "B8D0EB",
    "bg": "F0F5FB",
    "titleFont": "Montserrat",
    "bodyFont": "Be Vietnam Pro"
  },
  "style": "soft",
  "rectRadius": 0.1,
  "pageBadge": "circle"
}
```

### Step 2: Each compile.js in the series loads the same config

```javascript
const config = require('../series-config.json');
const theme = config.theme;
// All slides in this deck use the same theme from config
```

### Directory structure for a series
```
my-training-series/
├── series-config.json        # Shared style — edit once, used by all
├── part-01-giao-tiep/
│   ├── slides/
│   │   ├── slide-01.js ... slide-06.js
│   │   └── compile.js        # loads ../series-config.json
│   └── output/
├── part-02-lam-viec-nhom/
│   ├── slides/
│   │   ├── slide-01.js ... slide-07.js
│   │   └── compile.js        # loads ../series-config.json
│   └── output/
└── part-03-lanh-dao/
    ├── slides/ ...
    └── output/
```

All parts share the same palette, fonts, corner radius, and page badge style. Just change the content per deck.

### Using series mode
When the user says "tạo thêm 1 bài trong series" or provides a series-config.json, load the config instead of choosing a new palette. This ensures visual consistency across all presentations in the series.

---

## Dependencies

```bash
npm install -g pptxgenjs                         # Slide creation
npm install -g react-icons react react-dom sharp  # Icons
pip install "markitdown[pptx]"                     # QA text extraction
```

Optional (for visual QA):

```bash
brew install libreoffice  # PDF conversion
brew install poppler      # PDF to images
```
