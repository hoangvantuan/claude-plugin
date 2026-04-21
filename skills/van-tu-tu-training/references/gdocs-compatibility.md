# Google Docs Compatibility — Rules cho Output Markdown

**Mục đích:** Tài liệu `.md` sinh ra phải upload lên Google Drive và **auto-convert sang Google Docs** mà không vỡ layout.

**Nguyên tắc gốc:** Google Docs chỉ hiểu các element **native** của nó (heading, paragraph, bullet, numbered list, checkbox, table, blockquote, bold, italic, inline code, code block, link, image). Mọi thứ khác bị convert thành plain text hoặc mất định dạng.

## 1. Element an toàn — Dùng thoải mái

| Element Markdown | Google Docs convert thành | Ghi chú |
|---|---|---|
| `# H1` → `###### H6` | Heading 1 → Heading 6 | Dùng đúng cấp bậc, không nhảy cóc |
| `**bold**` | Bold | OK |
| `*italic*` | Italic | OK |
| `[text](url)` | Hyperlink | Luôn dùng dạng markdown link, không dán URL trần |
| `` `inline code` `` | Font Courier, nền xám | OK |
| Bullet `- item` | Bullet list | Lồng nhiều cấp vẫn OK, nhưng ≤ 3 cấp để dễ đọc |
| Numbered `1. item` | Numbered list | OK |
| Task list `- [ ]` / `- [x]` | Checkbox native (tick được trong Docs) | OK — đã verify thực tế |
| `> quote` | Blockquote (thụt lề, chữ xám) | OK |
| Table markdown `\| a \| b \|` | Native Google Docs table | Xem Section 3 |
| ` ```lang ` code block | Bảng 1 cell nền xám, font Courier | Chỉ dùng cho CODE THẬT |
| Hình ảnh `![alt](url)` | Ảnh nhúng | URL phải public, không localhost |

## 2. Element CẤM — Tuyệt đối không dùng

### 2.1. ASCII art box / diagram

Lý do: font Google Docs không monospace mặc định → các ký tự `┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼` lệch hàng thê thảm.

**❌ SAI:**

```
┌─────────────────┬─────────────────┐
│ QUAN SÁT        │ PHÂN TÍCH       │
│ Hôm nay tôi... │ Tại sao vậy?    │
└─────────────────┴─────────────────┘
```

**✅ ĐÚNG — table markdown:**

```markdown
| Quan sát | Phân tích |
|----------|-----------|
| Hôm nay tôi thấy gì? | Tại sao vậy? |
```

### 2.2. Multi-column layout bằng khoảng trắng

Lý do: mọi ký tự space/tab cố định bị Docs "đè" theo font proportional → vỡ hàng.

**❌ SAI:**

```
CỘT TRÁI             CỘT PHẢI
Nội dung 1           Nội dung A
```

**✅ ĐÚNG:** Table markdown 2 cột.

### 2.3. ASCII tree (folder structure)

Lý do: giống ASCII art — lệch hàng khi đổi font.

**❌ SAI:**

```
khoa-hoc/
├── module-01/
│   └── 01-van/
└── module-02/
```

**✅ ĐÚNG — nested bullet:**

```markdown
- `khoa-hoc/`
  - `module-01/`
    - `01-van/`
  - `module-02/`
```

**Ngoại lệ:** Bắt buộc phải hiển thị tree → bọc trong code block. Docs giữ monospace trong code block. Vẫn khuyến nghị nested bullet vì dễ edit.

### 2.4. Mermaid diagram

Lý do: Docs không render Mermaid — chỉ hiện raw code text.

**❌ SAI:** Dán code Mermaid trực tiếp vào deliverable.

**✅ ĐÚNG:**

1. Render Mermaid tại https://mermaid.live → export PNG → upload Drive → dùng `![sơ đồ](url-anh)`.
2. Không render được → viết bảng "Từ → Đến".

Ví dụ thay diagram prerequisite bằng bảng:

```markdown
| Module | Prerequisite |
|---|---|
| Module 1 | (không) |
| Module 2 | Module 1 |
| Module 3 | Module 1, Module 2 |
```

### 2.5. HTML tags

Lý do: Docs không parse HTML — hiện raw tag hoặc bỏ hẳn.

**❌ SAI:** `<center>`, `<details>`, `<summary>`, `<sup>`, `<sub>`, `<img width="300">`, `<font>`.

**Ngoại lệ duy nhất:** `<br>` bên trong cell của bảng markdown — Docs convert thành xuống dòng, hoạt động ổn định.

**✅ ĐÚNG:** Dùng markdown thuần. Cần hiển thị thu gọn → tạo section riêng với heading, không dùng `<details>`.

### 2.6. Horizontal rule `---` (BA dấu gạch ngang liên tiếp)

Lý do: Docs convert `---` thành đường kẻ mảnh ngắn ngoài lề, khó nhìn và phá nhịp đọc. Đặc biệt lặp lại nhiều lần trong 1 tài liệu dài → rối mắt khi in hoặc đọc trên Docs.

**❌ SAI:**

```markdown
Phần 1 kết thúc.

---

Phần 2 bắt đầu.
```

**✅ ĐÚNG — dùng heading hoặc blank line:**

```markdown
Phần 1 kết thúc.

## Phần 2

Phần 2 bắt đầu.
```

Hoặc nếu không cần heading mới → chỉ 1 dòng blank line giữa các section là đủ.

**Ngoại lệ:** YAML frontmatter ở đầu file `.md` (giữa `---` đầu và `---` cuối) — giữ nguyên. Đây không phải horizontal rule, là syntax frontmatter.

### 2.7. Footnote `[^1]`

Lý do: Docs convert **một phần** — số footnote thường giữ, nhưng liên kết về footnote đáy có thể lệch. Không đảm bảo 100%.

**Khuyến nghị:** Viết trực tiếp "(xem ghi chú 1 cuối tài liệu)" + section `## Ghi chú` cuối file. Tránh dùng syntax footnote GFM.

### 2.8. Link relative path giữa các file `.md`

**Vấn đề nghiêm trọng** cho skill này vì `naming-convention.md` yêu cầu relative link giữa module ↔ module ↔ phase.

Lý do: khi upload bộ `.md` lên Drive, mỗi file convert thành 1 Google Docs **độc lập, có URL riêng**. Link `[Module 2](../module-02/README.md)` sẽ **KHÔNG resolve** — Docs mở trang trống hoặc lỗi 404.

**Giải pháp theo tình huống:**

| Tình huống | Cách làm |
|---|---|
| Dùng trong git/local/GitHub | Giữ relative link — chuẩn naming-convention |
| Upload lên Google Drive | Sau khi convert, thay relative link bằng Docs URL |
| Cả hai | Tạo file mục lục (tong-quan) chứa Docs URL; file con link về mục lục thay vì link chéo |

**Quy trình khi cần upload Drive:**

1. Upload tất cả `.md` sang Drive, convert sang Docs.
2. Copy Docs URL của từng file vào 1 bảng mapping.
3. Find-replace relative path bằng Docs URL trong các file gốc.
4. Re-upload phiên bản mới, hoặc edit trực tiếp trên Docs.

## 3. Rules cho bảng (Table)

- **Không merge cell** — Markdown table không hỗ trợ; dán lên Docs mỗi ô vẫn độc lập.
- **Không quá 6 cột** — vượt thì tràn lề giấy A4.
- **Header bắt buộc** — dòng đầu là heading bảng, không bỏ trống.
- **Xuống dòng trong cell** → dùng `<br>` (hoạt động ổn định) hoặc tách thành row mới.
- **Alignment** `:---:` hoạt động nhưng không đảm bảo 100% — đừng phụ thuộc.
- **1 cell = 1 ý ngắn** — không nhồi 3-4 câu vào 1 cell; nội dung dài tách thành heading + paragraph ngay dưới bảng.
- **Blank line trước và sau bảng** — bảng sát heading có thể bị render nhập vào heading.

## 4. Ký tự Unicode — Whitelist / Blacklist

**An toàn 100%:**

| Nhóm | Ký tự |
|---|---|
| Tick/Cross | ✓ ✗ ☐ ☑ ☒ |
| Mũi tên | → ← ↑ ↓ ↔ |
| Bullet visual | • · ◦ |
| Emoji cơ bản | ✅ ❌ ⚠️ 📌 💡 🎯 |

**CẤM (font fallback xấu):**

| Nhóm | Ký tự |
|---|---|
| Box drawing | `┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼` |
| Block elements | `█ ▓ ▒ ░` |

**Hạn chế (dùng khi thật sự cần):**

- Circled numbers: ① ② ③ — ưu tiên `1.` numbered list.

## 5. Heading — Cấp bậc & cách dùng

- File bắt đầu bằng `#` (H1) duy nhất 1 lần — tên tài liệu.
- Dưới đó: `##` (H2) cho section chính, `###` (H3) cho subsection.
- **Không nhảy cóc** — từ H2 không nhảy thẳng H4. Accessibility best practice.
- **Không in đậm heading** — viết `## Tiêu đề`, không `## **Tiêu đề**`. Heading đã bold sẵn.
- **Không đi quá sâu** — tránh `## 1.1.1. ...`; H4 là đủ sâu.
- **Blank line trước heading** — tránh heading dính vào đoạn văn phía trên.

## 6. Code block — Khi nào dùng

- **Chỉ dùng cho CODE THẬT**: bash, python, json, yaml, markdown example, cấu trúc folder (ngoại lệ).
- **Không dùng code block làm "hộp khung"** cho diagram/layout/ghi chú thường — dùng table/blockquote/bullet thay thế.
- Fence ngôn ngữ `` ```bash `` → Docs ignore tên, chỉ giữ monospace + background.

## 7. Blank line — Quy tắc khoảng trắng

- **1 blank line** giữa paragraph, giữa bullet list và paragraph, giữa table và heading.
- **Không dùng 2+ blank line liên tiếp** — Docs có thể convert thành đoạn trống dài bất thường.
- **Không bỏ blank line** trước heading hoặc trước/sau table — block có thể bị render nhập vào nhau.

## 8. Checklist trước khi bàn giao file `.md`

Mắt quét từng file, xác nhận:

- ☐ Không có ký tự box-drawing `┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼` ngoài code block.
- ☐ Không có multi-column bằng khoảng trắng.
- ☐ Folder tree (nếu có) trong code block hoặc nested bullet.
- ☐ Mermaid đã export ảnh hoặc thay bằng bảng "Từ → Đến".
- ☐ Không có HTML tags (trừ `<br>` trong cell bảng).
- ☐ **Không có `---` horizontal rule** trong content (YAML frontmatter là ngoại lệ).
- ☐ Không có footnote `[^1]` — chuyển section "Ghi chú" cuối file.
- ☐ Link chéo giữa file: đã xử lý plan (giữ relative cho Git, hoặc thay Docs URL cho Drive).
- ☐ Bảng ≤ 6 cột, không merge cell, mỗi cell 1 ý ngắn, có blank line trước và sau.
- ☐ Heading không nhảy cóc, không in đậm, H4 là đủ sâu.
- ☐ Link dạng `[text](url)`, không URL trần.
- ☐ Hình ảnh URL public (không `localhost`, không path local).
- ☐ Blank line giữa các block, không 2+ blank line liên tiếp.
- ☐ (Khuyến khích) test: upload 1 file lên Drive → mở bằng Google Docs → kiểm tra layout.

## 9. Quick reference — Mapping cấm → thay thế

| Element cấm | Thay bằng |
|---|---|
| ASCII box `┌─┐│└─┘` | Table markdown |
| ASCII tree `├── └──` | Nested bullet (hoặc code block nếu buộc) |
| Multi-column space | Table markdown 2+ cột |
| Mermaid diagram | Ảnh PNG (export mermaid.live) hoặc table quan hệ |
| HTML `<center>` `<details>` | Heading + paragraph thường |
| Horizontal rule `---` | Heading mới hoặc blank line |
| Footnote `[^1]` | Section "Ghi chú" cuối tài liệu |
| Box drawing █ ▓ | Bỏ hoàn toàn, dùng text |
| Relative link chéo file (khi up Drive) | Docs URL sau convert |

## 10. Test nhanh

Trước khi giao tài liệu cho user:

1. Upload 1 file đại diện lên Google Drive.
2. Right-click → "Mở bằng" → "Google Tài liệu".
3. Kiểm tra: heading đúng cấp? Bảng còn cấu trúc? Link click được? Checkbox tick được? Không có đường kẻ `---` thừa?
4. Có ảnh → ảnh load được?
5. Scroll đầu đến cuối — không chỗ nào phải zoom để đọc.

Fail bất kỳ bước nào → quay lại `.md` fix, upload lại.
