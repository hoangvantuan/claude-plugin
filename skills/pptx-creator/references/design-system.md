# Design System

## Color Palette Reference

Choose a palette that matches the topic. Each has 5 colors mapped to theme keys: `primary` (darkest) -> `secondary` -> `accent` -> `light` -> `bg` (lightest).

**Lưu ý:** Các màu trong bảng là bộ màu gốc (aesthetic order). Khi gán vào theme, **PHẢI sort theo brightness** — xem mục "Assigning palette colors to theme keys" bên dưới.

| # | Name | Color 1 | Color 2 | Color 3 | Color 4 | Color 5 | Best For |
|---|------|---------|---------|---------|---------|---------|----------|
| 1 | Modern Health | `006d77` | `83c5be` | `edf6f9` | `ffddd2` | `e29578` | Healthcare, wellness |
| 2 | Business Authority | `2b2d42` | `8d99ae` | `edf2f4` | `ef233c` | `d90429` | Finance, corporate |
| 3 | Natural Outdoor | `283618` | `606c38` | `dda15e` | `bc6c25` | `fefae0` | Environment, agriculture |
| 4 | Retro Academic | `780000` | `c1121f` | `003049` | `669bbc` | `fdf0d5` | Academic, history |
| 5 | Soft Creative | `cdb4db` | `ffc8dd` | `ffafcc` | `bde0fe` | `a2d2ff` | Fashion, kids |
| 6 | Bohemian Warm | `d4a373` | `ccd5ae` | `e9edc9` | `faedcd` | `fefae0` | Wedding, organic |
| 7 | Vibrant Tech | `023047` | `219ebc` | `8ecae6` | `ffb703` | `fb8500` | Startups, education |
| 8 | Craftsmanship | `414833` | `656d4a` | `7f5539` | `a68a64` | `ede0d4` | Coffee, artisan |
| 9 | Tech Night | `000814` | `001d3d` | `003566` | `ffc300` | `ffd60a` | Tech events, astronomy |
| 10 | Education Charts | `264653` | `2a9d8f` | `e76f51` | `f4a261` | `e9c46a` | Data, education |
| 11 | Forest ESG | `344e41` | `3a5a40` | `588157` | `a3b18a` | `dad7cd` | Landscape, ESG |
| 12 | Elegant Fashion | `4a5759` | `b0c4b1` | `dedbd2` | `edafb8` | `f7e1d7` | Fashion, gallery |
| 13 | Art Food | `540b0e` | `9e2a2b` | `335c67` | `e09f3e` | `fff3b0` | Food, art, culture |
| 14 | Luxury Mystery | `22223b` | `4a4e69` | `9a8c98` | `c9ada7` | `f2e9e4` | Jewelry, hotel |

### Additional Palettes (Vietnamese-Inspired)

| # | Name | primary | secondary | accent | light | bg | Best For |
|---|------|---------|-----------|--------|-------|-----|----------|
| 15 | Lotus Pink | `6B2737` | `B5485D` | `F2C4CE` | `FAE5EA` | `FFF8FA` | Vietnamese culture, events |
| 16 | Indigo Silk | `1B2A4A` | `2E4A7A` | `6B8FBF` | `B8D0EB` | `F0F5FB` | Professional, premium |
| 17 | Bamboo Green | `2D4A22` | `4A7A3A` | `8FBF6B` | `C5E0B3` | `F0F8EC` | Nature, sustainability |
| 18 | Golden Rice | `5C3D1E` | `8B6914` | `D4A940` | `F0D68A` | `FFF9E6` | Agriculture, tradition |

### Custom Color Palette

Người dùng có thể cung cấp bộ màu riêng thay vì chọn từ bảng có sẵn. Khi nhận được custom palette, map vào 5 theme keys theo quy tắc brightness:

```javascript
// User cung cấp: ["1A1A2E", "16213E", "0F3460", "E94560", "F5F5F5"]
const theme = {
  primary: "1A1A2E",    // Darkest
  secondary: "16213E",  // 2nd darkest
  accent: "E94560",     // Vibrant accent
  light: "0F3460",      // Mid-tone
  bg: "F5F5F5"          // Lightest
};
```

**Quy tắc khi user cung cấp custom palette:**
1. Yêu cầu tối thiểu 3 màu (primary, accent, bg), tối đa 5 màu
2. Nếu chỉ 3 màu → tự sinh secondary (trung gian primary-accent) và light (trung gian accent-bg)
3. Luôn sort theo brightness: darkest → lightest
4. Nếu bg quá tối (luminance < 70%) → cảnh báo và đề xuất thay bằng `"FAFAFA"`
5. Validate hex format: 6 ký tự, KHÔNG có `#`

### Custom Font

Người dùng có thể chỉ định font riêng cho title và body. Khi nhận custom font:

```javascript
// Gán trực tiếp vào theme object:
const theme = {
  // ...color keys...
  titleFont: "Oswald",           // Font cho tiêu đề
  bodyFont: "Source Sans Pro"    // Font cho nội dung
};
```

**Quy tắc:**
1. Cảnh báo nếu font không hỗ trợ tiếng Việt (dấu sắc, huyền, hỏi, ngã, nặng)
2. Font an toàn cho tiếng Việt: Be Vietnam Pro, Inter, Montserrat, Raleway, Roboto, Open Sans, Nunito
3. Nếu không chắc font hỗ trợ Vietnamese → đề xuất fallback `Be Vietnam Pro`
4. Title font nên là Bold/SemiBold weight, body font nên là Regular weight

### How to Choose

1. **Match the topic** — a healthcare presentation shouldn't use Tech Night palette
2. **Consider the audience** — corporate = muted palettes (#2, #14, #16), creative = vibrant (#5, #7)
3. **Dark vs light** — dark primary for title slides, light bg for content slides ("sandwich" structure)
4. **Vietnamese content** — palettes #15-18 are designed with Vietnamese aesthetics in mind
5. **Custom palette** — nếu user cung cấp bộ màu riêng, ưu tiên dùng thay vì chọn từ bảng

### Theme Object

Always use these exact 7 keys:
```javascript
const theme = {
  // Colors (5 keys)
  primary: "264653",    // Darkest — titles, dark backgrounds
  secondary: "2a9d8f",  // Dark accent — body text, icons
  accent: "e9c46a",     // Mid-tone — highlights, badges, borders
  light: "f4a261",      // Light accent — subtle fills, cards
  bg: "FAFAFA",         // Background — MUST be lightest, suitable for slide bg

  // Fonts (2 keys)
  titleFont: "Montserrat",      // Title + section headers
  bodyFont: "Be Vietnam Pro"    // Body, bullets, captions, page badge
};
```

**IMPORTANT: Assigning palette colors to theme keys:**
Do NOT blindly copy palette colors left-to-right. Sort by brightness:
- `primary` = darkest color in the palette
- `bg` = lightest color (or use `"FAFAFA"` / `"FFFFFF"` if no palette color is light enough)
- Remaining 3 colors fill `secondary`, `accent`, `light` by relative darkness

Example for palette #1 (006d77, 83c5be, edf6f9, ffddd2, e29578):
```javascript
// WRONG — blindly left-to-right:
{ primary: "006d77", secondary: "83c5be", accent: "edf6f9", light: "ffddd2", bg: "e29578" }
// e29578 (salmon) as bg is too dark!

// CORRECT — sorted by brightness:
{ primary: "006d77", secondary: "e29578", accent: "83c5be", light: "ffddd2", bg: "edf6f9" }
// edf6f9 (ice blue) is the lightest → perfect bg
```

**Color usage rules:**
- One color dominates (60-70% visual weight)
- 1-2 supporting tones
- 1 sharp accent for CTAs, badges, highlights
- `bg` must always be light enough for dark text to be readable on it
- NO gradients (PptxGenJS limitation) — use gradient images instead
- Opacity adjustments OK (0-100%)

---

## Font Reference

### Vietnamese-Optimized Font Pairings

Vietnamese diacritics (ă, ệ, ồ, ử, đ) require fonts with full Unicode support. These pairings are tested and confirmed:

| Header Font | Body Font | Vibe | Best For |
|-------------|-----------|------|----------|
| **Montserrat** | **Be Vietnam Pro** | Modern, clean | Business, tech, startup |
| **Inter** | **Be Vietnam Pro** | Neutral, versatile | Any topic |
| **Be Vietnam Pro Bold** | **Be Vietnam Pro Regular** | Unified, Vietnamese | Government, education |
| **Playfair Display** | **Be Vietnam Pro** | Elegant, editorial | Culture, fashion |
| **Raleway** | **Be Vietnam Pro** | Light, airy | Creative, marketing |

### Fallback Pairings (System Fonts)

If custom fonts are not installed, use these system fonts:

| Header Font | Body Font | Notes |
|-------------|-----------|-------|
| **Arial Black** | **Arial** | Universal, safe |
| **Georgia** | **Calibri** | Classic, readable |
| **Trebuchet MS** | **Calibri** | Modern system font |

### Typography Scale

| Element | Size | Weight | Notes |
|---------|------|--------|-------|
| Slide title | 36pt | Bold | Content slides cố định 36pt. Cover slide cho phép 44-60pt |
| Section header | 24pt | Bold | Tiêu đề phụ, đầu dòng section |
| Body text | 18-20pt | Regular | Nội dung chính, tối thiểu 18pt |
| Bullet items | 18-20pt | Regular | Cùng size body text |
| Footnotes/Captions | 14pt | Regular | Chú thích, nguồn, annotations |
| Large stat | 60-80pt | Bold | Số liệu nổi bật, key metrics |
| Page badge | 12pt | Bold | Bottom-right circle |

**Tỷ lệ typography**: Title (36) → Heading (24) → Body (18) → Footnote (14) giữ tỷ lệ ~1.5x giữa các cấp.

Body text at 14-16pt is too small for presentations — always use 18pt+ for text the audience reads.

### Typography Rules
- **Bold only for titles and headers** — body text stays regular weight
- **Left-align paragraphs and lists** — center only titles and stat callouts
- **Size contrast matters** — Title (36pt) cần đủ lớn so với Body (18pt) để tạo hierarchy
- **Font assignment** — `titleFont` cho title + heading, `bodyFont` cho body + footnote + badge
- **Line spacing** — use `paraSpaceAfter` instead of `lineSpacing` for bullets
- **charSpacing** (not `letterSpacing`) — for letter-spaced headings

---

## Style Recipes

4 design styles control corner radius and spacing. Pick one per presentation and commit to it.

### 1. Sharp & Compact
- **Rect Radius**: 0 - 0.05"
- **Spacing**: Tight (0.08-0.15" gaps)
- **Best for**: Data reports, tables, corporate, financial
- **Vibe**: Professional, no-nonsense, information-dense

```javascript
// Example: Sharp card
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1, w: 4, h: 3,
  fill: { color: "FFFFFF" },
  shadow: { type: "outer", color: "000000", blur: 4, offset: 1, angle: 135, opacity: 0.08 }
});
```

### 2. Soft & Balanced (Default)
- **Rect Radius**: 0.08 - 0.12"
- **Spacing**: Moderate (0.2-0.3" gaps)
- **Best for**: Corporate, training, education
- **Vibe**: Professional but approachable

```javascript
// Example: Soft card
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.5, y: 1, w: 4, h: 3,
  fill: { color: "FFFFFF" }, rectRadius: 0.1,
  shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.1 }
});
```

### 3. Rounded & Spacious
- **Rect Radius**: 0.15 - 0.25"
- **Spacing**: Loose (0.3-0.5" gaps)
- **Best for**: Product, marketing, creative pitches
- **Vibe**: Friendly, modern, tech-forward

```javascript
// Example: Rounded card
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.5, y: 1, w: 4, h: 3,
  fill: { color: "FFFFFF" }, rectRadius: 0.2,
  shadow: { type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.12 }
});
```

### 4. Pill & Airy
- **Rect Radius**: 0.3 - 0.5"
- **Spacing**: Very open (0.4-0.8" gaps)
- **Best for**: Brand launches, premium, keynotes
- **Vibe**: Sophisticated, spacious, Apple-like

```javascript
// Example: Pill badge
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1, y: 1, w: 2, h: 0.5,
  fill: { color: theme.accent }, rectRadius: 0.25
});
```

### Mixing Rule
Outer container radius must be >= inner element radius. Don't put a 0.3" pill inside a 0.1" card.

---

## Design Moods

Style Recipes xác định hình dạng (radius, spacing). Design Moods xác định **cảm xúc và tính cách** của presentation. Chọn 1 mood trước khi design.

| Mood | Đặc điểm | Color Tendency | Layout | Best For |
|------|-----------|----------------|--------|----------|
| **Corporate Authority** | Trang trọng, tin cậy, data-driven | Dark primary + neutral bg | Symmetric, grid-based | Báo cáo, tài chính, investor deck |
| **Startup Energy** | Táo bạo, tươi sáng, forward-looking | Vibrant accent + clean white bg | Asymmetric, spacious | Pitch deck, product launch |
| **Editorial Elegance** | Tinh tế, editorial, magazine-like | Muted tones + cream/warm bg | Asymmetric, lots of whitespace | Culture, fashion, luxury brands |
| **Playful Creative** | Vui tươi, năng động, colorful | Bold multi-color + light bg | Varied, card-heavy | Education, kids, marketing |
| **Minimal Zen** | Tối giản cực đoan, chỉ giữ essential | Monochrome + 1 accent | Very spacious, center-focus | Keynote, philosophy, premium |
| **Bold Brutalist** | Mạnh mẽ, raw, high-contrast | Black/white + 1 neon accent | Large type, overlapping elements | Tech, art, creative agencies |
| **Warm Storytelling** | Gần gũi, narrative, human | Earthy tones + warm bg | Image-heavy, flowing | Training, workshop, HR |
| **Data Dashboard** | Analytical, structured, dense | Cool blues/grays + white bg | Grid, charts-heavy, compact | Analytics, research, science |

### Mood → Style Recipe Mapping

| Mood | Recommended Style | Palette Range |
|------|-------------------|---------------|
| Corporate Authority | Sharp or Soft | #2, #14, #16 |
| Startup Energy | Rounded | #7, #10 |
| Editorial Elegance | Soft or Pill | #12, #14, custom muted |
| Playful Creative | Rounded or Pill | #5, #7, custom vibrant |
| Minimal Zen | Sharp | Monochrome + 1 accent |
| Bold Brutalist | Sharp | Black/white + neon custom |
| Warm Storytelling | Soft or Rounded | #6, #8, #15, #18 |
| Data Dashboard | Sharp or Soft | #9, #16, cool custom |

### Applying Moods

Mood ảnh hưởng đến mọi quyết định design:

```
Corporate Authority → formal titles, minimal decorative shapes, data-first
Startup Energy → bold hero images, large stat callouts, aspirational CTAs
Editorial Elegance → generous whitespace, serif title font (nếu hỗ trợ VN), image-text split
Playful Creative → colorful icon rows, card grids, varied backgrounds
Minimal Zen → 1-2 elements per slide, extreme whitespace, no decorative shapes
Bold Brutalist → oversized type, high contrast, overlapping text on shapes
Warm Storytelling → photos of people, narrative flow, warm palette throughout
Data Dashboard → charts on every content slide, dense but organized, cool tones
```

---

## Layout Guidelines

### Spacing
- **Minimum margins**: 0.5" from slide edges
- **Between content blocks**: 0.3-0.5"
- **Between icon and text**: 0.08-0.15"
- **Don't fill every inch** — whitespace is your friend

### Visual Balance
- **Dark/light contrast**: Dark bg for title + conclusion, light for content ("sandwich")
- **Visual motif**: Pick ONE distinctive element (rounded frames, icon circles, side borders) and repeat across all slides
- **Every slide needs a non-text visual** — image, chart, icon, or decorative shape

### Contrast Rules (CRITICAL)

**Rule: Every addText() call must pass this check:**
1. What is the DIRECT background of this text? (slide bg? shape fill? card fill?)
2. Is that background DARK (luminance < 50%) or LIGHT (luminance > 50%)?
3. Dark bg → text MUST be `"FFFFFF"` or `"F0F0F0"`. Light bg → text MUST be `"222222"` or `"333333"` or `theme.primary`.

**Safe text colors:**
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

**Quick test:** If the first 2 chars of the hex are 0-6 → it's dark → use light text. If A-F → it's light → use dark text.

**On cards/shapes:** Check text color against the SHAPE fill color, not the slide background behind it.

**Validation:** After writing each slide, scan every `addText()`. Ask: "Can I clearly read this text against its direct background?"

### Common Mistakes to Avoid
- Accent lines under titles (AI hallmark)
- Text-only slides (forgettable)
- Repeated same layout (monotonous)
- Centered body text (hard to read)
- Low contrast icons/text (light text on light bg, dark on dark)
- Mixing spacing randomly
- Styling one slide but leaving rest plain

---

## Anti-AI Slop Patterns

AI-generated slides có "dấu hiệu nhận dạng" khiến output trông generic. Tránh tất cả:

### Visual Patterns to AVOID

| Pattern | Vì sao xấu | Thay bằng |
|---------|------------|-----------|
| Accent line dưới mọi title | Hallmark #1 của AI slides | Font size contrast hoặc shape background |
| 3 icon cards đều nhau hàng ngang | Quá predictable | Vary size, dùng 2 hoặc 4, stagger vertically |
| Gradient purple-to-blue | Overused cliché | Palette cụ thể cho topic |
| Mọi slide cùng 1 layout | Monotonous | Alternate ít nhất 3 layout types |
| Decorative circles ngẫu nhiên | Vô nghĩa, clutter | Mỗi shape phải có mục đích |
| Subtitle italic nhạt dưới mọi title | Filler content | Chỉ dùng subtitle khi thực sự cần |
| Bullet points chiếm toàn slide | Text-heavy | Chia thành cards, icon rows, split layout |
| Stock photo placeholder rectangles | Lazy | AI-generated images hoặc meaningful shapes |

### Content Patterns to AVOID

| Pattern | Thay bằng |
|---------|-----------|
| Generic titles ("Giới thiệu", "Tổng quan") | Cụ thể: "3 Rào Cản Khiến Team Không Scale Được" |
| Mỗi slide có chính xác 3 bullets | Vary: 2 bullets + 1 visual, hoặc 1 big stat + context |
| "Cảm ơn!" slide trống | CTA cụ thể hoặc memorable closing statement |
| Density đều mỗi slide | Alternate dense (data) và sparse (divider/stat) |

### Self-Check Sau Mỗi Deck

1. "Bỏ logo, slide này có thể thuộc bất kỳ deck nào khác?" → Thiếu personality
2. "Đoán được layout slide tiếp theo?" → Thiếu variety
3. "Có slide nào chỉ toàn text?" → Cần visual element

---

## Background Techniques

PptxGenJS không hỗ trợ gradient fills, nhưng dùng **background images** để đạt hiệu ứng tương tự.

### Gradient Backgrounds (via AI-generated images)

Dùng `ai-multimodal` skill tạo gradient background:

```
Prompt examples:
- "Subtle gradient, dark navy (#1B2A4A) to medium blue (#2E4A7A), smooth horizontal, 1920x1080, no text"
- "Warm gradient, cream (#FFF9E6) to soft peach (#FFE5D0), vertical, minimal, 1920x1080"
- "Dark moody gradient, charcoal to deep teal, diagonal, 1920x1080"
```

```javascript
slide.background = { path: "./assets/gradient-navy.jpg" };
// Hoặc base64
slide.background = { data: "image/jpeg;base64,..." };
```

### Pattern/Texture Backgrounds

```
Prompt examples:
- "Subtle geometric pattern, thin lines, light gray on white, tileable, 1920x1080"
- "Soft paper texture, cream colored, minimal grain, 1920x1080"
- "Dot grid pattern, very subtle, light blue dots on white, 1920x1080"
```

### Background Strategy by Slide Type

| Slide Type | Background Approach |
|------------|-------------------|
| Cover | Gradient image hoặc dark solid + decorative shapes |
| Section Divider | Accent solid hoặc subtle gradient |
| Content | Light solid (`bg` key) hoặc subtle texture |
| Data/Chart | Clean white/light — không distract |
| Summary | Dark gradient hoặc accent (bookend với Cover) |

### Asset Workflow

1. Generate backgrounds TRƯỚC khi code slides (Step 2.5)
2. Save vào `assets/` directory cùng level với `slides/`
3. Consistent set cho cả deck — đừng mix nhiều style
4. Resolution: 1920x1080 (16:9 ratio)
5. File size: under 500KB/image

## Vietnamese Text Overflow

Vietnamese với dấu (ă, ệ, ồ, ử, ớ) cao và rộng hơn ASCII text ~30%. Kết hợp với font size lớn, text sẽ tràn box nếu không cẩn thận.

**Quy tắc:**

1. **Size text boxes rộng hơn** — thêm 30% chiều cao so với English. Title 2 dòng ở 44pt cần ~1.4" height (không phải 1.0").

2. **Giới hạn nội dung/slide** — với body 18-20pt, tối đa 4-5 bullet points hoặc 3 content blocks. Nếu dài → tách 2 slides.

3. **Dùng `fit: true` cho auto-shrink** khi text có thể tràn:
   ```javascript
   slide.addText("Tiêu đề có thể dài", {
     x: 0.5, y: 0.5, w: 9, h: 1.2,
     fontSize: 44, fontFace: "Be Vietnam Pro",
     fit: true  // auto-shrink if text overflows
   });
   ```

4. **Text box height guidelines:**

   | Font Size | 1 line | 2 lines | 3 lines |
   |-----------|--------|---------|---------|
   | 36pt title | 0.7" | 1.3" | 1.9" |
   | 24pt heading | 0.5" | 0.95" | 1.4" |
   | 20pt body | 0.45" | 0.8" | 1.15" |
   | 14pt footnote | 0.35" | 0.6" | 0.85" |

5. **Giữ text ngắn gọn** — mỗi block tối đa 1-2 câu. Không nhồi đoạn văn dài vào slide.
