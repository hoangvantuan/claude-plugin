# Shun Claude Plugin

Plugin package cho Claude Code — phát triển các **skills**, **agents**, **hooks**, và **MCP servers** mở rộng khả năng của Claude Code.

## Installation

```bash
claude plugin install gh:hoangvantuan/shun-claude-plugin
```

## Components

### Skills

| Skill | Description |
| --- | --- |
| `ghost-blog` | Ghost CMS blog management |
| `outline-writer` | Content analysis & outline creation (presentation/blog/doc) |
| `slidev-builder` | Slidev presentation builder from outline — theme selection, PDF export |
| `writer-agent` | Document transformation and article writing (v2.0.0 — tier workflows, preset presets, enhanced insights) |
| `prompt-generator` | Meta-prompting — tạo prompt chất lượng cao, giảm hallucination |
| `prompt-generator-v2` | KERNEL framework — prompt engineering nâng cao (94% first-try success, prompt chaining, verification criteria) |
| `viral-post-creator` | Tạo bài đăng viral trên social media (3 archetype) |
| `youtube-title-generator` | Tạo tiêu đề YouTube hấp dẫn từ ý tưởng nội dung |
| `creative-thought-partner` | Đối tác tư duy sáng tạo — brainstorming & insight discovery |
| `deep-post-ideas` | Trích xuất outline bài đăng từ tài liệu tham khảo |
| `deep-learner` | Học hiểu sâu nội dung — tạo tài liệu học có cấu trúc 6 phase |
| `content-planner` | Lên kế hoạch và viết bài Facebook + Blog — 2-phase workflow (Plan → Write) |
| `things-manager` | Quản lý Things 3 tasks, projects, areas, tags qua things-cli (Go CLI) |
| `pinchtab` | Browser automation cho AI agents — điều khiển Chrome qua PinchTab HTTP API (navigate, click, fill form, scrape, multi-tab) |
| `facebook` | Facebook automation via PinchTab — đăng bài lên wall, tag bạn bè, quản lý nội dung Facebook |
| `wisdom-mentor` | Trò chuyện với người thầy tri thức — Naval Ravikant, Daniel Schmachtenberger, Csikszentmihalyi, Krishnamurti, Ken Wilber, Thích Viên Minh, Trần Việt Quân, Thích Nhất Hạnh, Sư Tâm Pháp |
| `work-explainer` | Personal teacher — giải thích công việc đã làm qua 9-step framework (approach, tradeoffs, mistakes, transferable lessons) |
| `van-tu-tu-training` | Xây dựng bộ tài liệu training theo mô hình Văn-Tư-Tu (Tam Tuệ Học) — kiến trúc modular, tỷ lệ 10-20-70, templates đầy đủ cho VĂN/TƯ/TU |
| `workshop-builder` | Thiết kế workshop hoàn chỉnh theo Backwards Design + 4Cs + Kirkpatrick — 5 giai đoạn (Vision → Design → Prepare → Deliver → Follow-up) |

### Agents

_Coming soon_ — Các agent chuyên biệt cho các workflow phức tạp.

### Hooks

_Coming soon_ — Các hook scripts chạy tự động theo sự kiện của Claude Code.

### MCP Servers

_Coming soon_ — Các MCP server cung cấp tool integration cho Claude Code.

## Development

Khi tạo skill mới, luôn sử dụng `/skill-creator` để bắt đầu:

```
/skill-creator
```

Skill creator sẽ hướng dẫn cấu trúc chuẩn và tạo các file cần thiết.

## License

MIT
