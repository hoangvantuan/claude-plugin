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
| `ai-artist` | Tạo ảnh qua Nano Banana, 129 curated prompts, validation interview, 3 modes (search/creative/wild) |
| `anti-ai-writing` | Rules viết tiếng Việt không giống AI, blacklist từ/cụm/chấm câu, self-critique bắt buộc. Dùng độc lập hoặc làm baseline cho mọi task viết |
| `content-planner` | Lên dàn ý, lập kế hoạch nội dung chi tiết cho bài Blog. Chỉ planning, không viết bài |
| `creative-thought-partner` | Đối tác tư duy sáng tạo, brainstorming & insight discovery |
| `deep-insight` | Quan sát đa chiều → Phân tích tách lớp → Đúc kết cốt lõi, hiểu sâu vấn đề qua chu trình 3 bước |
| `deep-learner` | Dẫn dắt từng bước hiểu sâu bản chất nội dung, 4 lớp hiểu + áp dụng đời sống |
| `facebook` | Facebook automation via PinchTab, đăng bài lên wall, tag bạn bè |
| `game-theory-lens` | Phân tích chủ đề qua lăng kính Game Theory, nhận diện players/strategies/payoffs, Nash equilibrium, mechanism design |
| `ghost-blog` | Ghost CMS blog management |
| `outline-writer` | Content analysis & outline creation (presentation/blog/doc) |
| `pinchtab` | Browser automation cho AI agents, điều khiển Chrome qua PinchTab HTTP API |
| `pptx-creator` | Tạo PowerPoint đẹp, chuyên nghiệp, hỗ trợ font tiếng Việt (PptxGenJS) |
| `problem-solving` | Kỹ thuật giải quyết vấn đề có hệ thống, inversion, collision-zone, scale-game, simplification cascades |
| `prompt-generator` | Meta-prompting, tạo prompt chất lượng cao |
| `prompt-generator-v2` | KERNEL framework, prompt engineering nâng cao |
| `sequential-thinking` | Phân tích từng bước cho vấn đề phức tạp, revision, branching, hypothesis verification |
| `skill-auto-improver` | Phân tích và cải tiến skill tự động, quality audit + improvement patterns |
| `social-post` | Viết bài social đa platform (Facebook, Threads, LinkedIn, Zalo) chia sẻ góc nhìn chiều sâu, anti-AI rules, self-critique |
| `style-writer` | Skill viết lách hợp nhất (từ style-library + style-dna), 2 workflow: Analyze (bóc tách DNA văn phong) + Writer (viết nội dung theo voice/persona/structure). Gồm personas, 7 voices, 8 structures |
| `substack-tools` | Quản lý bài viết Substack: draft, schedule, publish, list, sections + scan/crawl newsletter khác |
| `systems-thinking` | Phân tích tư duy hệ thống theo framework Donella Meadows, feedback loops, system traps, leverage points |
| `things-manager` | Quản lý Things 3 tasks, projects, areas, tags qua things-cli (Go CLI) |
| `van-tu-tu-training` | Xây dựng tài liệu training theo mô hình Văn-Tư-Tu (Tam Tuệ Học), kiến trúc modular, tỷ lệ 10-20-70, templates đầy đủ |
| `wisdom-mentor` | Trò chuyện với người thầy tri thức (28 mentors) |
| `work-explainer` | Personal teacher, giải thích công việc đã làm qua 9-step framework |
| `workshop-builder` | Thiết kế workshop theo Backwards Design + 4Cs + Kirkpatrick |
| `writer-planner` | Xử lý input (PDF, DOCX, EPUB, URL, YouTube) và tạo kế hoạch chia bài viết, convert → analyze → plan. Tier workflows |
| `youtube-title-generator` | Tạo tiêu đề YouTube hấp dẫn từ ý tưởng nội dung |

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
