# PptxGenJS API Reference

Complete API reference for creating slides with PptxGenJS. Read this before writing any slide code.

## Setup

```javascript
const pptxgen = require("pptxgenjs");
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';  // 10" x 5.625"
pres.author = 'Author';
pres.title = 'Title';

let slide = pres.addSlide();
// ... add content ...
pres.writeFile({ fileName: "output.pptx" });
```

**Layout dimensions** (coordinates in inches):
- `LAYOUT_16x9`: 10" x 5.625" (default, recommended)
- `LAYOUT_16x10`: 10" x 6.25"
- `LAYOUT_4x3`: 10" x 7.5"
- `LAYOUT_WIDE`: 13.3" x 7.5"

---

## Text

```javascript
// Basic text
slide.addText("Title", {
  x: 0.5, y: 0.5, w: 9, h: 1,
  fontSize: 36, fontFace: "Be Vietnam Pro",
  color: "264653", bold: true, align: "center", valign: "middle"
});

// Character spacing (NOT letterSpacing — that is silently ignored)
slide.addText("SPACED", { x: 1, y: 1, w: 8, h: 1, charSpacing: 6 });

// Rich text (mixed formatting)
slide.addText([
  { text: "Bold ", options: { bold: true } },
  { text: "Italic ", options: { italic: true } },
  { text: "Normal" }
], { x: 1, y: 2, w: 8, h: 1 });

// Multi-line (requires breakLine: true)
slide.addText([
  { text: "Dong 1", options: { breakLine: true } },
  { text: "Dong 2", options: { breakLine: true } },
  { text: "Dong 3" }  // last item doesn't need breakLine
], { x: 0.5, y: 0.5, w: 8, h: 2 });

// Text box margin — set 0 for precise alignment with shapes
slide.addText("Title", { x: 0.5, y: 0.3, w: 9, h: 0.6, margin: 0 });

// Auto-shrink text to fit box (prevents overflow — use for Vietnamese)
slide.addText("Tiêu đề có thể dài với nhiều dấu tiếng Việt", {
  x: 0.5, y: 0.5, w: 9, h: 1.2,
  fontSize: 44, fontFace: "Be Vietnam Pro",
  fit: true  // auto-shrinks font if text overflows the box
});
```

**Vietnamese text sizing tip:** Vietnamese diacritics (ă, ệ, ồ, ử) add ~30% extra height. Always size text boxes generously or use `fit: true` to auto-shrink.

## Bullets & Lists

```javascript
// Bullet list
slide.addText([
  { text: "Muc thu nhat", options: { bullet: true, breakLine: true } },
  { text: "Muc thu hai", options: { bullet: true, breakLine: true } },
  { text: "Muc thu ba", options: { bullet: true } }
], { x: 0.5, y: 1, w: 8, h: 3, fontSize: 16, fontFace: "Be Vietnam Pro" });

// NEVER use unicode bullets like "•" — creates double bullets

// Sub-items
{ text: "Sub-item", options: { bullet: true, indentLevel: 1 } }

// Numbered list
{ text: "First", options: { bullet: { type: "number" }, breakLine: true } }
```

## Shapes

```javascript
// Rectangle
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1, w: 4, h: 3,
  fill: { color: "FF0000" },
  line: { color: "000000", width: 2 }
});

// Oval / Circle
slide.addShape(pres.shapes.OVAL, { x: 1, y: 1, w: 2, h: 2, fill: { color: "0088CC" } });

// Line
slide.addShape(pres.shapes.LINE, {
  x: 1, y: 3, w: 5, h: 0,
  line: { color: "CCCCCC", width: 1, dashType: "dash" }
});

// Rounded rectangle (use rectRadius)
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1, y: 1, w: 4, h: 2,
  fill: { color: "FFFFFF" }, rectRadius: 0.1
});

// Transparency
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "0088CC", transparency: 50 }
});

// Shadow — create fresh object EVERY TIME (see pitfalls)
const makeShadow = () => ({
  type: "outer", color: "000000", blur: 6,
  offset: 2, angle: 135, opacity: 0.15
});
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "FFFFFF" },
  shadow: makeShadow()
});
```

**Shadow properties:**

| Property | Type | Range | Notes |
|----------|------|-------|-------|
| `type` | string | `"outer"`, `"inner"` | |
| `color` | string | 6-char hex | No `#`, no 8-char |
| `blur` | number | 0-100 pt | |
| `offset` | number | 0-200 pt | Must be non-negative |
| `angle` | number | 0-359 degrees | 135 = bottom-right, 270 = upward |
| `opacity` | number | 0.0-1.0 | Use this for transparency |

**Available shapes:** RECTANGLE, OVAL, LINE, ROUNDED_RECTANGLE

**No gradient fills** — use a gradient image as background instead.

---

## Images

```javascript
// From file path
slide.addImage({ path: "images/photo.png", x: 1, y: 1, w: 5, h: 3 });

// From URL
slide.addImage({ path: "https://example.com/image.jpg", x: 1, y: 1, w: 5, h: 3 });

// From base64 (faster, no file I/O)
slide.addImage({ data: "image/png;base64,iVBORw0KGgo...", x: 1, y: 1, w: 5, h: 3 });

// Options
slide.addImage({
  path: "image.png", x: 1, y: 1, w: 5, h: 3,
  rotate: 45, rounding: true, transparency: 50,
  altText: "Mo ta hinh anh",
  hyperlink: { url: "https://example.com" }
});

// Sizing modes
{ sizing: { type: 'contain', w: 4, h: 3 } }  // fit inside
{ sizing: { type: 'cover', w: 4, h: 3 } }    // fill area (may crop)

// Calculate aspect ratio
const calcWidth = maxHeight * (origWidth / origHeight);
const centerX = (10 - calcWidth) / 2;
```

---

## Icons (react-icons)

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaCheckCircle } = require("react-icons/fa");

function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

// Usage
const iconData = await iconToBase64Png(FaCheckCircle, "#4472C4", 256);
slide.addImage({ data: iconData, x: 1, y: 1, w: 0.5, h: 0.5 });
```

**Note:** Use size 256+ for crisp icons. The `size` controls rasterization resolution, not display size on slide (that's `w` and `h`).

**Icon libraries:** `react-icons/fa` (Font Awesome), `react-icons/md` (Material), `react-icons/hi` (Heroicons), `react-icons/bi` (Bootstrap)

---

## Slide Backgrounds

```javascript
slide.background = { color: "F1F1F1" };
slide.background = { color: "FF3399", transparency: 50 };
slide.background = { path: "https://example.com/bg.jpg" };
slide.background = { data: "image/png;base64,iVBORw0KGgo..." };
```

---

## Tables

```javascript
// Simple table
slide.addTable([
  ["Header 1", "Header 2"],
  ["Cell 1", "Cell 2"]
], {
  x: 1, y: 1, w: 8, h: 2,
  border: { pt: 1, color: "999999" },
  fill: { color: "F1F1F1" }
});

// Styled table
let tableData = [
  [
    { text: "Header", options: { fill: { color: "264653" }, color: "FFFFFF", bold: true } },
    { text: "Header 2", options: { fill: { color: "264653" }, color: "FFFFFF", bold: true } }
  ],
  ["Row 1 Col 1", "Row 1 Col 2"],
  [{ text: "Merged", options: { colspan: 2 } }]
];
slide.addTable(tableData, { x: 1, y: 2, w: 8, colW: [4, 4] });
```

---

## Charts

```javascript
// Bar chart
slide.addChart(pres.charts.BAR, [{
  name: "Doanh thu", labels: ["Q1", "Q2", "Q3", "Q4"],
  values: [4500, 5500, 6200, 7100]
}], {
  x: 0.5, y: 1, w: 9, h: 4, barDir: 'col',
  showTitle: true, title: 'Doanh Thu Theo Quy'
});

// Line chart
slide.addChart(pres.charts.LINE, [{
  name: "Users", labels: ["T1", "T2", "T3"], values: [1000, 2500, 4200]
}], { x: 0.5, y: 1, w: 9, h: 4, lineSize: 3, lineSmooth: true });

// Pie chart
slide.addChart(pres.charts.PIE, [{
  name: "Share", labels: ["A", "B", "C"], values: [35, 45, 20]
}], { x: 2, y: 1, w: 6, h: 4, showPercent: true });
```

### Modern Chart Styling

Default charts look dated. Apply these for a clean look:

```javascript
slide.addChart(pres.charts.BAR, chartData, {
  x: 0.5, y: 1, w: 9, h: 4, barDir: "col",
  chartColors: ["2a9d8f", "264653", "e9c46a"],
  chartArea: { fill: { color: "FFFFFF" }, roundedCorners: true },
  catAxisLabelColor: "64748B",
  valAxisLabelColor: "64748B",
  valGridLine: { color: "E2E8F0", size: 0.5 },
  catGridLine: { style: "none" },
  showValue: true,
  dataLabelPosition: "outEnd",
  dataLabelColor: "1E293B",
  showLegend: false
});
```

**Chart types:** BAR, LINE, PIE, DOUGHNUT, SCATTER, BUBBLE, RADAR

---

## Slide Masters

```javascript
pres.defineSlideMaster({
  title: 'TITLE_SLIDE',
  background: { color: '264653' },
  objects: [{
    placeholder: {
      options: { name: 'title', type: 'title', x: 1, y: 2, w: 8, h: 2 }
    }
  }]
});

let slide = pres.addSlide({ masterName: "TITLE_SLIDE" });
slide.addText("Tieu De", { placeholder: "title" });
```

---

## Critical Pitfalls

These cause file corruption or visual bugs. Memorize them.

### 1. NEVER use `#` in hex colors
```javascript
color: "FF0000"      // CORRECT
color: "#FF0000"     // CORRUPTS FILE
```

### 2. NEVER use 8-char hex for opacity
```javascript
// WRONG — corrupts file
shadow: { color: "00000020" }

// CORRECT — use opacity property
shadow: { color: "000000", opacity: 0.12 }
```

### 3. NEVER reuse option objects
PptxGenJS mutates objects in-place. Sharing causes corruption.

```javascript
// WRONG
const shadow = { type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 };
slide.addShape(pres.shapes.RECTANGLE, { shadow, ... });
slide.addShape(pres.shapes.RECTANGLE, { shadow, ... }); // corrupted!

// CORRECT — factory function
const makeShadow = () => ({ type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 });
slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
```

### 4. Use `bullet: true`, NEVER unicode "•"
Unicode bullets create double bullets in PowerPoint.

### 5. Use `breakLine: true` between array items
Without it, multi-line text runs together on one line.

### 6. Avoid `lineSpacing` with bullets
Causes excessive gaps. Use `paraSpaceAfter` instead.

### 7. Each presentation needs fresh pptxgen() instance
Don't reuse across multiple files.

### 8. Don't pair ROUNDED_RECTANGLE with rectangular accent borders
Rectangular overlays won't cover rounded corners. Use RECTANGLE for both.

### 9. Shadow offset must be non-negative
Negative values corrupt the file. Use `angle: 270` for upward shadows.

### 10. createSlide() must be synchronous
NO async/await in slide creation functions. PptxGenJS operations are blocking.
