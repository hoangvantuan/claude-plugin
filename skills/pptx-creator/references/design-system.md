# Design System

## Color Palette Reference

Choose a palette that matches the topic. Each has 5 colors mapped to theme keys: `primary` (darkest) -> `secondary` -> `accent` -> `light` -> `bg` (lightest).

| # | Name | primary | secondary | accent | light | bg | Best For |
|---|------|---------|-----------|--------|-------|-----|----------|
| 1 | Modern Health | `006d77` | `83c5be` | `edf6f9` | `ffddd2` | `e29578` | Healthcare, wellness |
| 2 | Business Authority | `2b2d42` | `8d99ae` | `edf2f4` | `ef233c` | `d90429` | Finance, corporate |
| 3 | Natural Outdoor | `606c38` | `283618` | `fefae0` | `dda15e` | `bc6c25` | Environment, agriculture |
| 4 | Retro Academic | `780000` | `c1121f` | `fdf0d5` | `003049` | `669bbc` | Academic, history |
| 5 | Soft Creative | `cdb4db` | `ffc8dd` | `ffafcc` | `bde0fe` | `a2d2ff` | Fashion, kids |
| 6 | Bohemian Warm | `ccd5ae` | `e9edc9` | `fefae0` | `faedcd` | `d4a373` | Wedding, organic |
| 7 | Vibrant Tech | `8ecae6` | `219ebc` | `023047` | `ffb703` | `fb8500` | Startups, education |
| 8 | Craftsmanship | `7f5539` | `a68a64` | `ede0d4` | `656d4a` | `414833` | Coffee, artisan |
| 9 | Tech Night | `000814` | `001d3d` | `003566` | `ffc300` | `ffd60a` | Tech events, astronomy |
| 10 | Education Charts | `264653` | `2a9d8f` | `e9c46a` | `f4a261` | `e76f51` | Data, education |
| 11 | Forest ESG | `dad7cd` | `a3b18a` | `588157` | `3a5a40` | `344e41` | Landscape, ESG |
| 12 | Elegant Fashion | `edafb8` | `f7e1d7` | `dedbd2` | `b0c4b1` | `4a5759` | Fashion, gallery |
| 13 | Art Food | `335c67` | `fff3b0` | `e09f3e` | `9e2a2b` | `540b0e` | Food, art, culture |
| 14 | Luxury Mystery | `22223b` | `4a4e69` | `9a8c98` | `c9ada7` | `f2e9e4` | Jewelry, hotel |

### Additional Palettes (Vietnamese-Inspired)

| # | Name | primary | secondary | accent | light | bg | Best For |
|---|------|---------|-----------|--------|-------|-----|----------|
| 15 | Lotus Pink | `6B2737` | `B5485D` | `F2C4CE` | `FAE5EA` | `FFF8FA` | Vietnamese culture, events |
| 16 | Indigo Silk | `1B2A4A` | `2E4A7A` | `6B8FBF` | `B8D0EB` | `F0F5FB` | Professional, premium |
| 17 | Bamboo Green | `2D4A22` | `4A7A3A` | `8FBF6B` | `C5E0B3` | `F0F8EC` | Nature, sustainability |
| 18 | Golden Rice | `5C3D1E` | `8B6914` | `D4A940` | `F0D68A` | `FFF9E6` | Agriculture, tradition |

### How to Choose

1. **Match the topic** — a healthcare presentation shouldn't use Tech Night palette
2. **Consider the audience** — corporate = muted palettes (#2, #14, #16), creative = vibrant (#5, #7)
3. **Dark vs light** — dark primary for title slides, light bg for content slides ("sandwich" structure)
4. **Vietnamese content** — palettes #15-18 are designed with Vietnamese aesthetics in mind

### Theme Object

Always use these exact 5 keys:
```javascript
const theme = {
  primary: "264653",    // Darkest — titles, dark backgrounds
  secondary: "2a9d8f",  // Dark accent — body text, icons
  accent: "e9c46a",     // Mid-tone — highlights, badges, borders
  light: "f4a261",      // Light accent — subtle fills, cards
  bg: "FAFAFA"          // Background — MUST be lightest, suitable for slide bg
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

Vietnamese diacritics (a, e, o, u, d) require fonts with full Unicode support. These pairings are tested and confirmed:

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
| Slide title | 40-48pt | Bold | Main heading, never < 36pt |
| Section header | 24-28pt | Bold | Subsections |
| Body text | 18-22pt | Regular | Main content, 18pt minimum, 20pt preferred |
| Bullet items | 18-20pt | Regular | Same as body |
| Captions | 13-14pt | Regular | Muted color, small annotations only |
| Large stat | 60-80pt | Bold | Big numbers, key metrics |
| Page badge | 12pt | Bold | Bottom-right circle |

Body text at 14-16pt is too small for presentations — always use 18pt+ for text the audience reads.

### Typography Rules
- **Bold only for titles and headers** — body text stays regular weight
- **Left-align paragraphs and lists** — center only titles and stat callouts
- **Size contrast matters** — titles need 36pt+ to stand out from 14-16pt body
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

### Contrast Rules

Text must always be readable against its background. Apply these pairings:

| Background | Text Color | Example |
|------------|-----------|---------|
| Dark (primary, secondary) | `"FFFFFF"` or `"F0F0F0"` | White/light text |
| Light (bg, light) | `"222222"` or `theme.primary` | Dark text |
| Accent fill (cards, badges) | Check manually | Depends on accent brightness |

**Quick test:** If the first 2 chars of the hex are 0-6 → it's dark → use light text. If A-F → it's light → use dark text.

**On cards/shapes:** The text must contrast with the SHAPE fill color, not the slide background behind it.

### Common Mistakes to Avoid
- Accent lines under titles (AI hallmark)
- Text-only slides (forgettable)
- Repeated same layout (monotonous)
- Centered body text (hard to read)
- Low contrast icons/text (light text on light bg, dark on dark)
- Mixing spacing randomly
- Styling one slide but leaving rest plain
