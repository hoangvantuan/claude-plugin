# Thiết kế: `project-memory` — Bộ nhớ tri thức tự cải tiến cấp dự án

- Ngày: 2026-06-05
- Trạng thái: Đã duyệt thiết kế, chờ viết plan
- Skill liên quan đã có: `skill-auto-improver` (cải tiến 1 skill), `skill-creator` (tạo skill)

## 1. Mục tiêu

Xây một skill portable tên `project-memory` đóng vai bộ nhớ tri thức cho dự án đang làm. Nó gom bài học và context rời rạc vào một kho có index routing, đúc kết định kỳ thành tri thức sạch, và làm nền cho việc cải tiến dự án.

Cái lõi: **tách 2 pha rõ ràng**.
- Pha tri thức: capture (ghi) → consolidate (đúc kết).
- Pha thực thi: tách riêng, do người dùng kích hoạt, không bao giờ tự động nối tiếp consolidation.

Một skill điều phối cả vòng đời: ghi → đúc kết → (khi cần) thực thi.

## 2. Ràng buộc cốt lõi

1. **Skill chạy độc lập.** Không gọi `skill-auto-improver` hay `skill-creator` (máy khác có thể không cài). `project-memory` tự chứa đủ hướng dẫn tối thiểu để thực thi.
2. **Cơ chế portable, dữ liệu theo repo.** Skill nằm trong `skills/project-memory/`, dùng được cho mọi dự án. Dữ liệu memory ghi vào `memory/` ở thư mục gốc của repo đang mở.
3. **Progressive disclosure.** Đọc `index.md` (nhẹ) trước, chỉ load file entry chi tiết khi cần.
4. **Phân biệt Skill (Công cụ) vs Workflow (Bản đồ).** Skill = tool, trả lời "làm việc này thế nào". Workflow = map, trả lời "khi nào dùng tool nào, theo thứ tự ra sao". Schema entry phải phản ánh khác biệt này.
5. **Hành động khó đảo ngược phải có user duyệt.** Merge, archive làm mất/đổi entry gốc, luôn duyệt trước khi script chạy.

## 3. Taxonomy: 3 loại bản chất

Bốn nhóm thông tin cần quản lý quy về 3 loại bản chất:

| Nhóm gốc | Loại bản chất | Prefix ID | Trả lời câu hỏi |
|----------|---------------|-----------|-----------------|
| Skill cần cải tiến | **Tool** (subtype `improve`) | `T-` | Làm việc X thế nào? |
| Skill mới nên tạo | **Tool** (subtype `new`) | `T-` | Làm việc X thế nào? |
| Workflow lặp lại | **Map** | `M-` | Khi nào dùng tool nào, thứ tự ra sao? |
| Context rời rạc | **Fact** | `F-` | Cần nhớ gì khi làm? |

Khác biệt schema mấu chốt: **Map** ghi *trình tự + tool dùng ở mỗi bước*; **Tool** ghi *cách làm + contract*; **Fact** ghi *sự kiện + khi nào liên quan*.

## 4. Kiến trúc

```mermaid
flowchart LR
    subgraph CAPTURE["Pha 1: Capture (ghi)"]
        A1["/project-memory capture<br/>(thủ công)"]
        A2["Claude gợi ý<br/>cuối phiên"]
    end
    subgraph STORE["Bộ nhớ (memory/ ở gốc repo)"]
        IDX["index.md<br/>(bảng routing)"]
        ENT["entries/*.md<br/>(1 file / entry)"]
        ARC["archive/"]
    end
    subgraph CONSOL["Pha 2: Consolidate (đúc kết)"]
        C1["gộp trùng + đúc kết"]
        C2["phát hiện pattern"]
        C3["dọn rác + archive"]
    end
    RECALL["/project-memory recall<br/>(đọc khi làm việc)"]
    EXEC["Thực thi tự chứa<br/>(spec hành động rõ)"]

    A1 --> ENT
    A2 --> ENT
    ENT -.->|"frontmatter"| IDX
    IDX --> RECALL
    ENT --> CONSOL
    CONSOL --> ENT
    CONSOL --> ARC
    CONSOL -->|"entry consolidated"| EXEC
```

### 4.1. Bố cục thư mục

```
skills/project-memory/
  SKILL.md
  references/
    schemas.md            # schema chi tiết 3 loại entry + index
    consolidation.md      # quy trình consolidate chi tiết
    capture-signals.md    # tín hiệu nhận biết đáng capture
    self-contained-exec.md# checklist tối thiểu cải tiến/tạo skill, không gọi skill ngoài
  scripts/
    new-entry.py
    reindex.py
    archive.py

<project-root>/
  memory/
    index.md
    entries/
    archive/
```

## 5. Schema dữ liệu

### 5.1. `memory/index.md`

```markdown
# Memory Index — <tên dự án>

## 🔧 Tools (skill cải tiến + skill mới)
| ID | Tiêu đề | Loại | Status | Tags | File |
|----|---------|------|--------|------|------|
| T-001 | style-writer thiếu ví dụ voice | improve | raw | style-writer | [↗](entries/T-001.md) |

## 🗺️ Maps (workflow lặp lại)
| ID | Tiêu đề | Status | Tags | File |
|----|---------|--------|------|------|
| M-001 | Quy trình tạo skill mới end-to-end | raw | skill-dev | [↗](entries/M-001.md) |

## 📌 Facts (context rời rạc)
| ID | Tiêu đề | Status | Tags | File |
|----|---------|--------|------|------|
| F-001 | gws CLI dùng --params JSON | raw | gdrive | [↗](entries/F-001.md) |
```

Index chỉ chứa metadata đủ để route. `status`: `raw` → `consolidated` → `archived`.

### 5.2. Entry — Tool (`T-xxx`)

```markdown
---
id: T-001
type: tool
subtype: improve   # improve | new
status: raw
created: 2026-06-05
source: conversation   # conversation | manual
tags: [style-writer]
related: [T-005, M-002]
---
## Vấn đề / Cơ hội
Tool yếu chỗ nào, hoặc khoảng trống năng lực cần tool mới.
## Bài học gốc
Tình huống thực tế phát sinh insight.
## Contract đề xuất (làm gì, không phải làm sao)
Input / Output / ranh giới của tool.
## Hành động (khi execute)
Bước cụ thể, tự chứa, không gọi skill ngoài.
```

### 5.3. Entry — Map (`M-xxx`)

```markdown
---
id: M-001
type: map
status: raw
created: 2026-06-05
tags: [skill-dev]
related: []
---
## Mục tiêu workflow
Đạt được gì khi chạy hết bản đồ này.
## Trigger
Khi nào kích hoạt workflow này.
## Trình tự (bản đồ)
1. Bước A — dùng tool/skill nào — output gì
2. Bước B — dùng tool/skill nào — output gì
## Cạm bẫy / lưu ý
Chỗ hay sai khi chạy.
```

### 5.4. Entry — Fact (`F-xxx`)

```markdown
---
id: F-001
type: fact
status: raw
created: 2026-06-05
tags: [gdrive]
related: []
---
## Sự kiện / quy tắc
Nội dung fact.
## Khi nào liên quan
Tình huống fact này hữu ích.
## Nguồn
Vì sao ghi lại.
```

## 6. Ba thao tác

### 6.1. capture

Hai ngả, cùng đổ về `memory/entries/`:
- **Thủ công**: gọi `/project-memory capture` hoặc nói "ghi nhớ cái này". Claude hỏi gọn (type? tiêu đề?), đoán type/tags từ ngữ cảnh, chạy `new-entry.py`, điền nội dung, reindex.
- **Gợi ý cuối phiên**: khi task kết thúc, Claude quét hội thoại tìm tín hiệu đáng ghi, liệt kê đề xuất "nên capture X vào nhóm Y", **user duyệt** rồi mới ghi. Không tự ghi lén.

Tín hiệu nhận biết (chi tiết trong `references/capture-signals.md`):
- Gặp gotcha mất thời gian thử sai → **Fact**.
- Làm một trình tự 2+ lần → **Map**.
- Skill có sẵn yếu / thiếu năng lực → **Tool**.

### 6.2. consolidate (chạy thủ công)

```mermaid
flowchart TD
    S1["Đọc index, lọc entry status=raw"] --> S2["Nhóm theo type + tags + related"]
    S2 --> S3["Gộp trùng: merge entry cùng chủ đề<br/>→ viết lại 1 entry gọn, status=consolidated"]
    S3 --> S4["Phát hiện pattern: ≥3 entry<br/>cùng trỏ 1 gốc → tạo entry tổng hợp mới"]
    S4 --> S5["Đề xuất archive: entry đã xong/lỗi thời"]
    S5 --> S6["User duyệt từng đề xuất"]
    S6 --> S7["script: archive + reindex"]
```

Chốt:
- Consolidation **dừng ở tầng tri thức**, không tự thực thi. Output là entry `consolidated` sạch + danh sách pattern.
- Mọi thay đổi cấu trúc (merge, archive) **user duyệt trước**. Script chỉ chạy sau khi duyệt.
- Khi gộp, entry gốc **không xóa thẳng** mà chuyển `archive/` (giữ vết).

### 6.3. recall (progressive disclosure)

- `/project-memory recall [query]` → đọc **chỉ `index.md`** trước, match theo type/tags/tiêu đề, rồi **chỉ load file entry liên quan**.
- Tự động gợi recall: đầu phiên hoặc khi bắt đầu task khớp tag, Claude chủ động "memory có N entry liên quan, đọc không?".

## 7. Phân vai LLM vs script

| Việc | Ai làm |
|------|--------|
| Tạo file entry mới, cấp ID tăng dần | script (`new-entry.py`) |
| Regenerate `index.md` từ frontmatter | script (`reindex.py`) |
| Archive entry, đổi status | script (`archive.py`) |
| Gộp trùng, đúc kết, phát hiện pattern | LLM |
| Quyết định entry nào nên archive | LLM đề xuất, user duyệt, script thực thi |

Lý do: bảng index dễ lệch nếu sửa tay. Script quét frontmatter rồi dựng lại bảng, luôn đồng bộ. LLM khỏi gõ lại bảng.

Đặc tả script:
- `new-entry.py <type> <subtype>` — tạo file entry skeleton + cấp ID, in path.
- `reindex.py` — quét `memory/entries/` + `memory/archive/`, dựng lại `index.md`.
- `archive.py <id>` — chuyển entry sang archive, đổi status, gọi reindex.

## 8. Thực thi tự chứa (không phụ thuộc skill ngoài)

- Entry **Tool** chứa sẵn **Contract đề xuất** + **Hành động** đủ rõ. Khi execute, Claude đọc entry và làm trực tiếp bằng năng lực chung (sửa SKILL.md, tạo skill theo cấu trúc chuẩn trong CLAUDE.md). `SKILL.md` của `project-memory` nhúng checklist tối thiểu "cách cải tiến/tạo skill" (trong `references/self-contained-exec.md`).
- Entry **Map** chính là playbook tái dùng: gặp lại trigger, Claude đọc Map và chạy theo trình tự. Map tự nó là thực thi.
- Execution là **pha tách riêng**, user kích hoạt (ví dụ `recall T-001` rồi "làm theo entry này"). Consolidation không bao giờ tự nhảy sang execute.

## 9. Ranh giới với skill có sẵn

- `skill-auto-improver`: đi sâu cải tiến *1 skill* theo 11 nguyên lý.
- `project-memory`: đứng *trên*, là bộ nhớ + định tuyến đa nhóm cho cả dự án.

Hai cái bổ sung, không trùng. `project-memory` tự chứa phần execute tối thiểu nên chạy được kể cả khi máy không có `skill-auto-improver`/`skill-creator`.

## 10. Hạng mục cho plan triển khai

1. `SKILL.md` — workflow 3 thao tác + tín hiệu capture + checklist execute tự chứa.
2. `references/schemas.md`, `consolidation.md`, `capture-signals.md`, `self-contained-exec.md`.
3. Scripts: `new-entry.py`, `reindex.py`, `archive.py`.
4. Cập nhật `CLAUDE.md` + `README.md` (thêm skill mới vào danh sách).
