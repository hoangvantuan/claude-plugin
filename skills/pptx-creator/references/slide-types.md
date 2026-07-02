# Slide Types

Every slide MUST be classified as exactly one of these 5 types. This prevents "layout drift" and ensures visual variety.

---

## 1. Cover Page

The opening slide sets the tone for the entire presentation.

**Required elements:**
- Title (36pt bold, hoặc lớn hơn cho dramatic effect lên đến 60pt)
- Subtitle or tagline (18pt, muted color)
- Optional: author name, date, logo

**NO page badge on cover slides.**

**Layout options:**

### Center Layout
```
+------------------------------------------+
|                                          |
|                                          |
|          TIÊU ĐỀ THUYẾT TRÌNH           |
|          Phụ đề ở đây                    |
|          Tác giả • Ngày                  |
|                                          |
+------------------------------------------+
```
Dark background with light text. Simple, impactful.

### Split Layout
```
+------------------------------------------+
|  TIÊU ĐỀ        |                       |
|  THUYẾT TRÌNH    |     [Hình/Shape]      |
|                  |                       |
|  Phụ đề          |                       |
|  Tác giả • Ngày  |                       |
+------------------------------------------+
```
Text left (60%), visual right (40%). Or flip.

### Full Bleed Image
```
+------------------------------------------+
|  [Ảnh nền toàn slide]                    |
|                                          |
|          TIÊU ĐỀ (trắng trên overlay)   |
|          Phụ đề                          |
|                                          |
+------------------------------------------+
```
Image covers entire slide. Semi-transparent overlay for text readability.

---

## 2. Table of Contents

Navigation slide showing 3-5 sections.

**Required elements:**
- Section numbers or icons
- Section titles
- Optional: brief descriptions
- Page badge (required)

**Layout options:**

### Numbered List
```
+------------------------------------------+
|  Nội Dung Chính                          |
|                                          |
|  01  Giới thiệu tổng quan               |
|  02  Phân tích thị trường                |
|  03  Giải pháp đề xuất                   |
|  04  Kế hoạch triển khai                 |
|  05  Kết luận                        [3] |
+------------------------------------------+
```

### Card Grid
```
+------------------------------------------+
|  Nội Dung                                |
|                                          |
|  +--------+  +--------+  +--------+     |
|  |  01    |  |  02    |  |  03    |     |
|  | Giới   |  | Phân   |  | Giải   |     |
|  | thiệu  |  | tích   |  | pháp   |     |
|  +--------+  +--------+  +--------+     |
|                                      [2] |
+------------------------------------------+
```

---

## 3. Section Divider

Transition slides between major sections. Keep minimal.

**Required elements:**
- Section number (large, 60-72pt)
- Section title (24pt bold)
- Optional: 1-line description
- Page badge (required)

**Layout options:**

### Center Emphasis
```
+------------------------------------------+
|                                          |
|              01                          |
|         Giới Thiệu                       |
|    Tổng quan về dự án và mục tiêu        |
|                                          |
|                                      [3] |
+------------------------------------------+
```
Dark or accent background. Large section number.

### Left-Aligned
```
+------------------------------------------+
|                                          |
|  01                                      |
|  ----                                    |
|  Giới Thiệu Tổng Quan                   |
|  Mô tả ngắn gọn về phần này             |
|                                          |
|                                      [3] |
+------------------------------------------+
```
Accent line or shape as separator.

---

## 4. Content Page

The workhorse — 9 subtypes (4a-4i) to maintain visual variety.

**All content slides require:**
- Non-text visual element (image, chart, icon, or shape)
- Page badge (required)

### 4a. Text + Icon Rows
```
+------------------------------------------+
|  Lợi Ích Chính                           |
|                                          |
|  [icon]  Tiết kiệm thời gian            |
|          Mô tả chi tiết lợi ích...       |
|                                          |
|  [icon]  Tăng năng suất                  |
|          Mô tả chi tiết lợi ích...       |
|                                          |
|  [icon]  Giảm chi phí                    |
|          Mô tả chi tiết lợi ích...   [5] |
+------------------------------------------+
```
Icon in colored circle + bold header + description.

**Height Budget:** Max 3-4 rows. 3×0.85" + 2×0.15" = 2.85" ✓. Dùng `calcStack(3, 0.85)`.

### 4b. Two-Column (Text + Image)
```
+------------------------------------------+
|  Tiêu Đề Slide                           |
|                                          |
|  Nội dung văn bản  |  +-----------+     |
|  bên trái với      |  |           |     |
|  các điểm chính:   |  |  [Hình]   |     |
|  - Điểm 1          |  |           |     |
|  - Điểm 2          |  +-----------+     |
|  - Điểm 3          |                     |
|                                      [6] |
+------------------------------------------+
```

**Height Budget:** Dùng `calcColumns(2)` — text 55%, image 45%. Full safe area height.

### 4c. Data Visualization
```
+------------------------------------------+
|  Kết Quả Kinh Doanh Q4                  |
|                                          |
|  +-----------------------------+        |
|  |                             |        |
|  |     [Bar/Line/Pie Chart]    |        |
|  |                             |        |
|  +-----------------------------+        |
|  Nhận xét chính bên dưới biểu đồ    [7] |
+------------------------------------------+
```

### 4d. Big Stat Callout
```
+------------------------------------------+
|  Thành Tựu Nổi Bật                      |
|                                          |
|     95%          2.5M         30+        |
|   Hài lòng     Người dùng   Quốc gia   |
|                                          |
|   Bối cảnh ngắn về những con số này      |
|                                      [8] |
+------------------------------------------+
```
Large numbers (60-72pt) with small labels below (14pt).

**Height Budget:** Max 3 stat blocks. 3×1.1" + 2×0.2" = 3.7" ✓. Dùng `calcColumns(3)` — mỗi cột chứa number + label.

### 4e. Comparison / Before-After
```
+------------------------------------------+
|  So Sánh Giải Pháp                       |
|                                          |
|  +----------+      +----------+         |
|  |  Trước   |      |  Sau     |         |
|  |          |      |          |         |
|  | - Mục 1  |      | - Mục 1  |         |
|  | - Mục 2  |      | - Mục 2  |         |
|  +----------+      +----------+         |
|                                      [9] |
+------------------------------------------+
```

**Height Budget:** Dùng `calcColumns(2)` — 2 cột bằng nhau. Full safe area height.

### 4f. Timeline / Process Flow
```
+------------------------------------------+
|  Quy Trình Triển Khai                    |
|                                          |
|  [1]---->[2]---->[3]---->[4]            |
|  Khảo    Thiết   Phát    Triển          |
|  sát     kế      triển   khai           |
|                                          |
|                                     [10] |
+------------------------------------------+
```

**Height Budget:** Max 3-5 steps. Dùng `calcColumns(count)` — mỗi cột chứa icon + label. 1 row, chiều cao cố định ~2".

### 4g. Asymmetric Hero (phá grid)
```
+------------------------------------------+
|                                          |
|  +------------------+                    |
|  | BIG VISUAL       |  Key insight text  |
|  | (70% width)      |  nhỏ bên phải      |
|  | image/shape/     |  với 2-3 dòng      |
|  | chart            |  context        [7] |
|  +------------------+                    |
+------------------------------------------+
```
Visual chiếm 60-70% slide, text nhỏ bên cạnh. Tạo focal point mạnh.

### 4h. Staggered Cards
```
+------------------------------------------+
|  Tiêu Đề                                |
|                                          |
|  +--------+                              |
|  | Card 1 |  +--------+                  |
|  +--------+  | Card 2 |  +--------+     |
|              +--------+  | Card 3 |     |
|                          +--------+ [8] |
+------------------------------------------+
```
Cards xếp lệch (stagger y position), phá vỡ sự đều đặn. Mỗi card offset y thêm 0.3-0.5".

**Height Budget:** Max 3 cards. 3×1.0" + 2×0.1" + stagger offset (0.3") = 3.5" ✓. Dùng `calcColumns(3)` cho x positions, tự thêm stagger y offset. **CẢNH BÁO:** Tổng chiều cao PHẢI tính cả stagger offset.

### 4i. Full-Width Statement
```
+------------------------------------------+
|                                          |
|                                          |
|  "Một câu statement mạnh chiếm           |
|   toàn bộ chiều ngang slide"             |
|                                          |
|   — Attribution hoặc context nhỏ     [9] |
+------------------------------------------+
```
Quote lớn (28-36pt) + attribution nhỏ. Dùng cho insight quan trọng giữa các content slides. Background dark hoặc accent.

---

## 5. Summary / Closing

Wrap-up slides. Leave a lasting impression.

**Required elements:**
- Key takeaways or call-to-action
- Page badge (required)

**Layout options:**

### Key Takeaways
```
+------------------------------------------+
|  Tổng Kết                                |
|                                          |
|  1. Insight chính thứ nhất               |
|  2. Insight chính thứ hai                |
|  3. Insight chính thứ ba                 |
|                                          |
|  Bước tiếp theo / Kêu gọi hành động [12]|
+------------------------------------------+
```

### Thank You / Contact
```
+------------------------------------------+
|                                          |
|           Cảm Ơn!                        |
|                                          |
|     email@company.com                    |
|     +84 xxx xxx xxx                      |
|     company.com                          |
|                                     [12] |
+------------------------------------------+
```
Dark background, centered, minimal.

---

## Visual Rhythm Checklist (3 trục)

Rule "không lặp layout liên tiếp" còn mờ. Trục cụ thể hơn: khi plan outline, label mỗi slide theo **3 trục độc lập**, đảm bảo có biến thiên xuyên deck.

### Trục 1: Background tone (dark vs light)

Dark slide tạo "moment", light slide chứa nội dung dài. Deck 100% light = đều đều, mệt mắt. Deck 100% dark = nặng nề, khó đọc bullet.

**Quy tắc:** Mỗi 4-5 slides có ít nhất 1 dark slide. Cover thường dark, Section Divider thường dark hoặc accent, Summary thường dark (bookend với Cover).

### Trục 2: Density (sparse vs dense)

Sparse slide cho audience nghỉ mắt. Dense slide truyền thông tin. Xen kẽ tạo nhịp.

| Density | Slide types | Đặc điểm |
|---------|-------------|----------|
| **Sparse** | Cover, Divider, 4i Full-Width Statement, 4d Big Stat | 1-3 elements, whitespace ≥50% |
| **Medium** | TOC, 4a Icon Rows, 4f Timeline, Summary Takeaways | 4-7 elements, whitespace 30-50% |
| **Dense** | 4b Two-Column, 4c Data Viz, 4e Comparison, 4h Staggered Cards | 8+ elements, whitespace ≤30% |

**Quy tắc:** Không 2 dense slides liên tiếp. Pattern lý tưởng: Sparse → Medium → Dense → Sparse (chu kỳ 4 slides).

### Trục 3: Type scale (normal vs hero text)

Hero text = title 60pt+ hoặc statement chiếm ≥40% chiều cao slide. Tạo focal point mạnh, phá đều đặn.

| Type scale | Slide types | Title size |
|------------|-------------|-----------|
| **Normal** | TOC, 4a, 4b, 4c, 4e, 4f, Summary | Title 36pt cố định |
| **Hero** | Cover, Divider, 4d Big Stat, 4i Statement, 4g Asymmetric | Title 44-72pt hoặc text overlay lớn |

**Quy tắc:** Mỗi 5-6 slides có ít nhất 1 hero slide. Deck dài >12 slides cần ≥3 hero moments.

### Outline Rhythm Table

Khi plan outline (Step 4 của SKILL.md), điền bảng này cho cả deck:

| # | Slide | Type | Tone (D/L) | Density (S/M/D) | Scale (N/H) |
|---|-------|------|------------|-----------------|-------------|
| 1 | Cover | cover | D | S | H |
| 2 | TOC | toc | L | M | N |
| 3 | Divider 1 | divider | D | S | H |
| 4 | Vấn đề | 4a | L | M | N |
| 5 | Số liệu | 4d | L | S | H |
| ... | | | | | |

**Self-check sau khi điền:**

- Trục 1: có ít nhất 20% slides là Dark không?
- Trục 2: có 2 dense slides liên tiếp không? Nếu có → chèn sparse vào giữa.
- Trục 3: có ít nhất 1 hero moment mỗi 5 slides không?

Nếu fail bất kỳ trục nào → rework outline trước khi sang Step 5.

## Enforcement Rules

1. **Classify every slide** before writing code
2. **Never repeat the same layout** on consecutive slides — if slide 5 is "Text + Image", slide 6 should be different
3. **Every content slide (type 4) needs a non-text visual** — icon, chart, image, or decorative shape
4. **Page badges on all slides EXCEPT cover** — dùng `PAGE_BADGE` constant từ layout-helpers.js
5. **Dramatic font size contrast** — at least 20% difference between title and body
6. **0.5" minimum margins** from all edges
7. **Left-align body text** — center only titles and stat callouts
8. **Use layout-helpers.js** — NEVER hardcode positions cho multiple elements. Dùng `calcStack`, `calcColumns`, `calcGrid`
9. **Check height budget** — verify N×itemH + (N-1)×gap ≤ 3.8" TRƯỚC khi code. `calcStack` sẽ throw nếu vượt
10. **All content elements MUST stay within y: 1.2"–5.0"** — vượt 5.0" sẽ overlap page badge
