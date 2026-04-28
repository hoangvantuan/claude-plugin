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
| `creative-thought-partner` | Đối tác tư duy sáng tạo, brainstorming & insight discovery |
| `deep-insight` | Quan sát đa chiều → Phân tích tách lớp → Đúc kết cốt lõi, hiểu sâu vấn đề qua chu trình 3 bước |
| `deep-learner` | Dẫn dắt từng bước hiểu sâu bản chất nội dung, 4 lớp hiểu + áp dụng đời sống |
| `facebook` | Facebook automation via PinchTab, đăng bài lên wall, tag bạn bè |
| `game-theory-lens` | Phân tích chủ đề qua lăng kính Game Theory, nhận diện players/strategies/payoffs, Nash equilibrium, mechanism design |
| `ghost-blog` | Ghost CMS blog management |
| `meeting-minutes` | 2 workflow: (1) Tạo biên bản họp từ transcript/ghi chú (quyết định, action items, pending/parking lot), (2) Phân tích hành vi giao tiếp (conflict avoidance, speaking ratio, filler words, active listening, facilitation style) |
| `outline-writer` | Phân tích nội dung & tạo outline thuần nội dung (sequence of sections; thesis, key arguments, evidence), không quyết định media (slide/blog/doc), không quy định cách viết/tone/style (đó là việc của writer) |
| `pexels-media` | Source ảnh/video royalty-free từ Pexels API: search, curated, popular, collections, multi-resolution download + sidecar metadata bắt buộc. Cần `PEXELS_API_KEY` |
| `pinchtab` | Browser automation cho AI agents, điều khiển Chrome qua PinchTab HTTP API |
| `planning-content` | Phân tích nội dung & lên outline ý chính cho từng bài. Hỗ trợ mọi input: topic, notes, URL, file (PDF/DOCX/EPUB), YouTube. Convert tài liệu, research, content map, tier processing cho tài liệu lớn. KHÔNG can thiệp cách viết/tone/style |
| `pptx-creator` | Tạo PowerPoint đẹp, chuyên nghiệp, hỗ trợ font tiếng Việt (PptxGenJS) |
| `problem-solving` | Kỹ thuật giải quyết vấn đề có hệ thống, inversion, collision-zone, scale-game, simplification cascades |
| `prompt-engineering` | Prompt engineering patterns: few-shot, chain-of-thought, template systems, system prompt design, agent prompting best practices, persuasion principles cho LLM interaction |
| `prompt-generator` | Meta-prompting, tạo prompt chất lượng cao |
| `prompt-generator-v2` | KERNEL framework, prompt engineering nâng cao |
| `sequential-thinking` | Phân tích từng bước cho vấn đề phức tạp, revision, branching, hypothesis verification |
| `skill-auto-improver` | Phân tích và cải tiến skill tự động, quality audit + improvement patterns |
| `social-post` | Viết bài social đa platform (Facebook, Threads, LinkedIn, Zalo) chia sẻ góc nhìn chiều sâu, anti-AI rules, self-critique |
| `style-writer` | Skill viết lách hợp nhất, 2 workflow: Writer (mặc định, viết nội dung theo voice + structure) + Analyze (bóc tách DNA văn phong → tạo voice mới). Gồm 7 voices generic + 8 structures |
| `substack-tools` | Quản lý bài viết Substack: draft, schedule, publish, list, sections + scan/crawl newsletter khác |
| `systems-thinking` | Phân tích tư duy hệ thống theo framework Donella Meadows, feedback loops, system traps, leverage points |
| `things-manager` | Quản lý Things 3 tasks, projects, areas, tags qua things-cli (Go CLI) |
| `van-tu-tu-training` | Xây dựng tài liệu training theo mô hình Văn-Tư-Tu (Tam Tuệ Học), kiến trúc modular, tỷ lệ 10-20-70, templates đầy đủ |
| `wisdom-mentor` | Trò chuyện với người thầy tri thức (28 mentors) |
| `work-explainer` | Personal teacher, giải thích công việc đã làm qua 9-step framework |
| `workshop-builder` | Thiết kế workshop theo Backwards Design + 4Cs + Kirkpatrick |
| `speech-to-text` | Chuyển file audio/video thành text kèm timestamps qua Soniox API, hỗ trợ 60+ ngôn ngữ, audio (mp3/wav/flac) + video (mp4/mov/mkv/avi) |
| `youtube-title-generator` | Tạo tiêu đề YouTube hấp dẫn từ ý tưởng nội dung |
| `youtube-transcript` | Tải transcript (phụ đề/captions) từ YouTube video qua yt-dlp, convert VTT sang plain text |

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
