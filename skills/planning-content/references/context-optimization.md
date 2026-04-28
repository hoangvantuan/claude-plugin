# Context Optimization Guide

## Problem: Unnecessary content.md Reads

### Common Mistake

```
Phase 4: Map Content
├─ Read structure.json (~1.3K words)      OK
└─ Read content.md (~24K words)           WASTE!
    └─ Loses 94% of context on duplicate data
```

**Tại sao sai:**
- `structure.json` đã chứa TOÀN BỘ thông tin cấu trúc (outline, word counts, critical sections)
- `content.md` chỉ cần đọc khi cần nội dung chi tiết cho outline
- Đọc cả hai lãng phí 90%+ context budget

### Correct Workflow

```
Phase 4.0: Tier Detection
└─ ONLY read structure.json
    ├─ Extract outline (section titles, word counts)
    ├─ Extract stats (word_count, heading_count)
    └─ Determine tier

Phase 4.1-4.2: Content Map & Outlines
└─ Dùng data từ structure.json
    └─ Đọc content.md KHI CẦN chi tiết cho outline cụ thể
    └─ Đọc theo offset/limit, KHÔNG đọc toàn bộ
```

## Context Budget Comparison

### Example: 34,889-word document

| Approach | Structure Scan | Planning | Total |
|----------|---------------|----------|-------|
| Sai | 37K (json + content) | 2K | **39K** |
| Đúng | 2K (json only) | 2K + selective reads | **~10K** |

**Tiết kiệm: ~75% context budget**

## What structure.json Contains

```json
{
  "stats": {
    "word_count": 34889,
    "heading_count": 82,
    "critical_count": 24,
    "estimated_articles": 6
  },
  "tier_recommendation": {
    "tier": 1,
    "reason": "Word count 34,889 < 50,000"
  },
  "direct_path": {
    "eligible": true,
    "capacity_ok": true
  },
  "outline": [
    {
      "level": 2,
      "text": "Section Title",
      "line": 3,
      "line_end": 34,
      "word_count": 1571,
      "critical": true
    }
  ],
  "suggested_chunks": [...]
}
```

**Đủ cho:**
- Xác định tier
- Tạo content map (từ outline)
- Lên outline cho từng bài
- Ước lượng số bài

## When to Read content.md

### OK

1. **Khi cần chi tiết cho outline**: đọc section cụ thể theo `line`/`line_end` từ structure.json
2. **Debug**: nếu structure.json thiếu hoặc lỗi

### KHÔNG đọc khi

1. **Phase 4.0**: Tier detection (dùng structure.json)
2. **Content map**: Listing sections (dùng outline từ JSON)
3. **Ước lượng số bài**: Dùng stats từ JSON

## Validation Checklist

- [ ] `structure.json` đã đọc
- [ ] `content.md` KHÔNG đọc toàn bộ ở Phase 4.0
- [ ] Content map tạo từ outline trong JSON
- [ ] Chỉ đọc content.md khi cần chi tiết cho outline cụ thể
