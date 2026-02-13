# Content Guidelines

## Source Fidelity

- Use ONLY source material, no fabrication
- **REWRITE ALL content in selected voice**: Source defines WHAT to say, Voice defines HOW to say it
- DO NOT copy-paste sentences from source (bao gồm cả ⭐ critical sections)
- Maintain original terminology (thuật ngữ giữ nguyên, nhưng câu văn phải được viết lại)
- ⭐ Critical sections: faithful rewrite, giữ 100% ý nghĩa, KHÔNG tóm tắt, viết lại bằng tiếng Việt + voice đã chọn
- Non-critical sections: MUST be rewritten in the selected voice's persona, structure, and language patterns
- VERIFY quotes prove source origin, but article content must be rewritten (not copied)

## Writing Quality

**Narrative Coherence:**

- Mỗi bài viết phải có mạch logic riêng, KHÔNG phải tóm tắt tuần tự từng section
- Sections phải nối với nhau bằng bridges (logical hoặc emotional), không phải "Tiếp theo..."
- Draw connections giữa các ý trong bài VÀ với thông điệp cốt lõi của series

**Opening & Closing (quyết định ấn tượng):**

- Opening: Hook compelling (câu hỏi, hình ảnh, khoảnh khắc). TRÁNH: "Trong bài này chúng ta sẽ..."
- Closing: Kết resonant (câu hỏi mở, hình ảnh, lời mời). TRÁNH: "Tóm lại, bài viết đã trình bày..."
- Mechanical phrases BLACKLIST: "Trong phần tiếp theo", "Như đã đề cập ở trên", "Bài viết này sẽ", "Tóm lại"

**Depth vs Breadth:**

- Khi một ý quan trọng: đi SÂU (ví dụ, implications, câu hỏi) thay vì liệt kê
- Khi nhiều ý nhỏ: nhóm lại thành pattern/theme, không liệt kê từng ý riêng lẻ
- Priority: 2-3 key insights explored deeply > 10 points listed superficially

**Reader Engagement:**

- Đặt câu hỏi cho người đọc (rhetorical hoặc reflective)
- Dùng ví dụ cụ thể, relatable thay vì abstract
- Tạo tension/curiosity trước khi giải đáp
- Vary sentence length: xen kẽ câu ngắn và dài

**Anti-AI Writing:** Canonical rules trong [article-writer-prompt.md#anti-ai-writing](article-writer-prompt.md). Tóm tắt: không em dash (—), không AI vocabulary, xen kẽ câu ngắn/dài, từ thuần Việt, cấu trúc câu Việt tự nhiên.

## Formatting

- Link between articles with relative paths
- Track all sections with [Sxx] IDs
- NO markdown tables in article output - use bullet points instead
- NO diagrams (mermaid, ASCII, flowcharts) - describe in prose or bullets

## Series List (MANDATORY)

- **MỖI bài viết PHẢI có "## Các bài viết trong series" ở cuối** - Thiếu = FAIL
- Mark current article with *(đang xem)*
- Validation: Subagent return format includes `SERIES_LIST: YES/NO`
- Main agent MUST check `SERIES_LIST: YES` trước khi accept article
