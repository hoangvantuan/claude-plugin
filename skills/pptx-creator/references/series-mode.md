# Series Mode — Multiple Presentations, Same Style

Khi tạo nhiều presentations trong cùng series (ví dụ: training Part 1, 2, 3), lưu style config 1 lần và reuse cho mọi deck.

## Step 1: Tạo `series-config.json` cho presentation đầu tiên

```json
{
  "series": "Kỹ Năng Mềm Training 2026",
  "mood": "Warm Storytelling",
  "styleRecipe": "soft",
  "theme": {
    "primary": "1B2A4A",
    "secondary": "2E4A7A",
    "accent": "6B8FBF",
    "light": "B8D0EB",
    "bg": "F0F5FB",
    "titleFont": "Montserrat",
    "bodyFont": "Be Vietnam Pro"
  }
}
```

**Schema fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `series` | string | yes | Tên series, hiển thị log khi compile |
| `mood` | string | yes | Tên mood từ design-system.md (Corporate Authority, Warm Storytelling, ...) |
| `styleRecipe` | string | yes | `sharp`, `soft`, `rounded`, `pill`. Slides tự enforce qua rectRadius và spacing |
| `theme` | object | yes | 7 keys (5 colors + 2 fonts) — compile.js load trực tiếp |

**Lưu ý:** `mood` và `styleRecipe` chỉ là metadata để slide author tham chiếu khi viết code. compile.js không enforce — slide files phải tự áp dụng nhất quán (rectRadius, spacing, decorative shape count).

## Step 2: Mỗi compile.js trong series load cùng config

```javascript
const config = require('../series-config.json');
const theme = config.theme;
// All slides in this deck use the same theme from config
```

## Directory structure

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
│   │   └── compile.js        # loads ../series-config.json
│   └── output/
└── part-03-lanh-dao/
    ├── slides/ ...
    └── output/
```

## Khi nào dùng

Khi user nói "tạo thêm 1 bài trong series" hoặc cung cấp `series-config.json` → load config thay vì chọn palette mới. Đảm bảo visual consistency.
