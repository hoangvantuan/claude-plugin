---
name: pptx-creator
description: "Create beautiful, professional PowerPoint presentations with Vietnamese font support and modern design. Use this skill any time a .pptx file needs to be created from scratch — slide decks, pitch decks, training materials, business presentations, or any PowerPoint creation task. Triggers on: PPTX, PowerPoint, presentation, slide deck, slides, tao slide, tao bai thuyet trinh, lam PowerPoint. This skill focuses on CREATING new presentations from scratch using PptxGenJS with a built-in design system optimized for Vietnamese content. For editing existing .pptx files, use the standard pptx skill instead."
---

# PPTX Creator

Tạo presentation đẹp, chuyên nghiệp với hỗ trợ font tiếng Việt.

## Quick Reference

| Item            | Spec                                            |
| --------------- | ----------------------------------------------- |
| Library         | PptxGenJS (Node.js)                             |
| Layout          | LAYOUT_16x9 (10" x 5.625")                      |
| Colors          | 6-char hex WITHOUT `#`                          |
| Vietnamese Font | Be Vietnam Pro                                  |
| English Font    | Inter / Montserrat                              |
| Theme Keys      | `primary`, `secondary`, `accent`, `light`, `bg` |
| Page Badge      | x: 9.3", y: 5.1" (all slides except Cover)      |


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

**First, check for series mode:** Look for `series-config.json` in the working directory or parent directory. If found, load it and skip Steps 2-3 — the style is already defined.

```bash
# Auto-detect series
ls series-config.json ../series-config.json 2>/dev/null
```

If no config found, read [references/design-system.md](references/design-system.md) for the full palette catalog and font pairings. Choose a palette that reflects the topic — don't default to generic blue.

### Step 3: Select Design Style

4 style recipes control corner radius and spacing. Read [references/design-system.md](references/design-system.md#style-recipes):

- **Sharp** (0-0.05") — data-dense reports, corporate
- **Soft** (0.08-0.12") — balanced, professional (default)
- **Rounded** (0.15-0.25") — marketing, product
- **Pill** (0.3-0.5") — premium, brand

### Step 4: Plan Slide Outline

Classify EVERY slide as one of 5 types. Read [references/slide-types.md](references/slide-types.md):

1. **Cover** — Opening slide, dramatic title
2. **Table of Contents** — Navigation, 3-5 sections
3. **Section Divider** — Transition between sections
4. **Content** — Main content (6 subtypes)
5. **Summary** — Closing, takeaways, CTA

**Enforce visual variety** — never repeat the same layout on consecutive slides.

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

  // Page badge (required for all except cover)
  slide.addShape(pres.shapes.OVAL, {
    x: 9.3, y: 5.1, w: 0.4, h: 0.4,
    fill: { color: theme.accent }
  });
  slide.addText(String(slideConfig.index), {
    x: 9.3, y: 5.1, w: 0.4, h: 0.4,
    fontSize: 12, fontFace: "Be Vietnam Pro",
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
    accent: "e9c46a", light: "f4a261", bg: "FAFAFA"
  };
  createSlide(pres, theme);
  pres.writeFile({ fileName: `slide-${String(slideConfig.index).padStart(2, '0')}-preview.pptx` });
}

module.exports = { createSlide, slideConfig };
```

**Use subagents**: Up to 5 slides can be generated concurrently via subagents. Each subagent receives the theme object and slide type specification.

### Step 6: Compile into Final PPTX

Use `scripts/compile.js` as the compilation template:

```javascript
const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Author Name';
pres.title = 'Presentation Title';

const theme = {
  primary: "264653",
  secondary: "2a9d8f",
  accent: "e9c46a",
  light: "f4a261",
  bg: "FAFAFA"
};

const slideCount = 10; // adjust to actual count
for (let i = 1; i <= slideCount; i++) {
  const num = String(i).padStart(2, '0');
  const slideModule = require(`./slide-${num}.js`);
  slideModule.createSlide(pres, theme);
}

pres.writeFile({ fileName: './output/presentation.pptx' });
```

Run: `cd slides && node compile.js`

### Step 7: QA (Required)

**Content QA:**

```bash
python -m markitdown output/presentation.pptx
python -m markitdown output/presentation.pptx | grep -iE "xxxx|lorem|ipsum|placeholder|TODO"
```

**Visual QA** (use subagent with fresh eyes):

```bash
# Convert to images for visual inspection
python scripts/office/soffice.py --headless --convert-to pdf output/presentation.pptx
pdftoppm -jpeg -r 150 output/presentation.pdf slide
```

Give the subagent this checklist:

- Overlapping elements or text overflow
- Low contrast (light on light / dark on dark)
- Uneven gaps or cramped sections
- Insufficient margins (< 0.5")
- Misaligned columns or cards
- Leftover placeholder content
- Font rendering issues with Vietnamese diacritics

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

- **Primary font**: `Be Vietnam Pro` — excellent Vietnamese diacritics, modern sans-serif
- **Fallback**: `Arial` — universal but less elegant
- **Title pairing**: `Montserrat` (header) + `Be Vietnam Pro` (body)
- **Alternative**: `Inter` (header) + `Be Vietnam Pro` (body)

### Theme Object Contract (5 Keys Only)

```javascript
const theme = {
  primary: "264653",    // Darkest — titles, dark backgrounds
  secondary: "2a9d8f",  // Dark accent — body text, icons
  accent: "e9c46a",     // Mid-tone — highlights, badges
  light: "f4a261",      // Light accent — subtle fills
  bg: "FAFAFA"          // Background — slide base color
};
```

NEVER use other key names. All slides receive this same object.

### File Corruption Prevention

Read [references/pptxgenjs-api.md](references/pptxgenjs-api.md#critical-pitfalls) for the full list. The top 3:

1. **NO `#` in hex colors** — `"FF0000"` not `"#FF0000"`
2. **NO 8-char hex** — use `opacity` property instead
3. **NO reusing option objects** — PptxGenJS mutates them. Create fresh each time.

### Font Size (Important — Text Must Be Readable)

Slide text must be large enough to read from a distance. These are MINIMUM sizes:

| Element | Size | Notes |
|---------|------|-------|
| Slide title | 40-48pt bold | Main heading, never smaller than 36pt |
| Section header | 24-28pt bold | Subsections |
| Body text | 18-22pt regular | Main content — 18pt minimum, 20pt preferred |
| Bullet items | 18-20pt | Same as body text |
| Captions/labels | 13-14pt | Muted color, small annotations only |
| Big stat numbers | 60-80pt bold | Key metrics, callout numbers |
| Page badge | 12pt | Bottom-right circle |

The most common mistake is body text at 14-16pt — this is too small for presentations. Always use 18pt+ for any text the audience needs to read.

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
   | 44pt title | 0.8" | 1.5" | 2.2" |
   | 28pt header | 0.6" | 1.1" | 1.6" |
   | 20pt body | 0.45" | 0.8" | 1.15" |
   | 14pt caption | 0.35" | 0.6" | 0.85" |

5. **Keep text concise** — Vietnamese descriptions should be 1-2 sentences max per block. Don't cram long paragraphs into slides.

6. **Test before finalizing** — always run markitdown + visual QA to catch overflow.

### Color Contrast (CRITICAL — Text Must Be Readable)

Poor contrast = invisible text. This is a mandatory checklist, not a guideline.

**Rule: Every addText() call must pass this check:**
1. What is the DIRECT background of this text? (slide bg? shape fill? card fill?)
2. Is that background DARK (luminance < 50%) or LIGHT (luminance > 50%)?
3. Dark bg → text MUST be `"FFFFFF"` or `"F0F0F0"`. Light bg → text MUST be `"222222"` or `"333333"` or `theme.primary`.

**Safe text colors — memorize these:**
```javascript
// ON DARK backgrounds (006d77, 2b2d42, 1B2A4A, 264653, etc.)
color: "FFFFFF"  // white — always safe on dark
color: "F0F0F0"  // off-white — always safe on dark

// ON LIGHT backgrounds (FAFAFA, F0F5FB, edf6f9, FFFFFF, ffddd2, etc.)
color: "222222"  // near-black — always safe on light
color: "333333"  // dark gray — always safe on light
color: theme.primary  // darkest theme color — safe on light
```

**NEVER do these:**
```
WRONG: "FFFFFF" text on "FAFAFA" bg (white on white)
WRONG: "FFFFFF" text on "edf6f9" bg (white on light blue)
WRONG: "83c5be" text on "edf6f9" bg (light teal on light blue)
WRONG: "ffddd2" text on "FFFFFF" bg (peach on white)
WRONG: theme.accent text when accent is a light color
```

**For shapes/cards:** Check text color against the SHAPE fill color, not the slide background. A white card on a dark slide still needs dark text inside the card.

**Validation step:** After writing each slide, scan every `addText()` call. Ask: "Can I clearly read this text against its direct background?" If no, fix it.

### Design Principles

- **Every slide needs a visual element** — image, chart, icon, or shape. No text-only slides.
- **Left-align body text** — center only titles
- **NEVER use accent lines under titles** — hallmark of AI-generated slides
- **Vary layouts** — don't repeat the same layout consecutively
- **60-70% primary color dominance** — 1-2 supporting, 1 sharp accent
- **0.5" minimum margins**, 0.3-0.5" between content blocks

---

## Series Mode (Multiple Presentations, Same Style)

When creating multiple presentations in a series (e.g., training Part 1, 2, 3), save the style config once and reuse it across all decks.

### Step 1: Create `series-config.json` for the first presentation

```json
{
  "series": "Kỹ Năng Mềm Training 2026",
  "theme": {
    "primary": "1B2A4A",
    "secondary": "2E4A7A",
    "accent": "6B8FBF",
    "light": "B8D0EB",
    "bg": "F0F5FB"
  },
  "style": "soft",
  "fonts": {
    "title": "Montserrat",
    "body": "Be Vietnam Pro"
  },
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
