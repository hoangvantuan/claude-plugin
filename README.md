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
| `openproject` | OpenProject API v3 integration |
| `ghost-blog` | Ghost CMS blog management |
| `outline-writer` | Content analysis & outline creation (presentation/blog/doc) |
| `slidev-builder` | Slidev presentation builder from outline — theme selection, PDF export |
| `writer-agent` | Document transformation and article writing (v2.0.0 — tier workflows, preset presets, enhanced insights) |
| `prompt-generator` | Meta-prompting — tạo prompt chất lượng cao, giảm hallucination |
| `viral-post-creator` | Tạo bài đăng viral trên social media (3 archetype) |
| `youtube-title-generator` | Tạo tiêu đề YouTube hấp dẫn từ ý tưởng nội dung |
| `creative-thought-partner` | Đối tác tư duy sáng tạo — brainstorming & insight discovery |
| `deep-post-ideas` | Trích xuất outline bài đăng từ tài liệu tham khảo |
| `deep-learner` | Học hiểu sâu nội dung — tạo tài liệu học có cấu trúc 6 phase |
| `content-planner` | Lên kế hoạch và viết bài Facebook + Blog — 2-phase workflow (Plan → Write) |
| `wisdom-mentor` | Trò chuyện với người thầy tri thức — Naval Ravikant, Daniel Schmachtenberger, Csikszentmihalyi, Krishnamurti, Ken Wilber |

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
