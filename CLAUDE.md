# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dự án phát triển các plugin cho Claude Code, bao gồm: **skills**, **agents**, **hooks**, và **MCP servers**. Mỗi plugin mở rộng khả năng của Claude Code cho các workflow chuyên biệt.

## Structure

```
.claude-plugin/plugin.json   # Plugin manifest
skills/                      # Các skill plugins (chi tiết xem ## Skill Structure)
  ai-artist/                 # Tạo ảnh qua Nano Banana — 129 curated prompts, validation interview, 3 modes
  anti-ai-writing/           # Rules viết tiếng Việt không giống AI — blacklist từ/cụm/chấm câu, self-critique, insight techniques (baseline cho mọi skill viết)
  codex-image/               # Tạo và chỉnh sửa ảnh qua OpenAI Codex CLI (gpt-image-2) — text-to-image, transparent bg (chroma-key), batch generation, image editing
  creative-thought-partner/  # Đối tác tư duy sáng tạo — brainstorming
  deep-insight/              # Quan sát đa chiều → Phân tích tách lớp → Đúc kết cốt lõi để hiểu sâu vấn đề
  deep-learner/              # Dẫn dắt từng bước hiểu sâu bản chất nội dung — 4 lớp hiểu + áp dụng đời sống
  deep-reader/               # Bộ 10 command phân tích đa chiều: summary, explain, insights, concept map, critique, article, video script, questions, checklist, gap analysis
  facebook/                  # Facebook automation via PinchTab (wall post, attach images, tag friends)
  game-theory-lens/          # Phân tích chủ đề qua lăng kính Lý thuyết Trò chơi (Game Theory)
  ghost-blog/                # Ghost CMS blog management
  meeting-minutes/           # 2 workflow: (1) Tạo biên bản họp, (2) Phân tích hành vi giao tiếp (insights) — conflict avoidance, speaking ratio, filler words, active listening, facilitation
  outline-writer/            # Phân tích nội dung & tạo outline thuần nội dung (sequence of sections; thesis, key arguments, evidence) — không quyết định media (slide/blog/doc), không quy định cách viết/tone/style
  pexels-media/              # Source ảnh/video royalty-free từ Pexels API — search, curated, collections, multi-resolution download + sidecar metadata bắt buộc
  pinchtab/                  # Browser automation for AI agents via PinchTab HTTP API
  planning-content/          # Phân tích nội dung & lên outline ý chính cho từng bài. Hỗ trợ mọi input: topic, notes, URL, file (PDF/DOCX/EPUB), YouTube. Convert tài liệu, research, content map, tier processing cho tài liệu lớn
  problem-solving/           # Kỹ thuật giải quyết vấn đề có hệ thống — inversion, collision-zone, scale-game
  pptx-creator/              # Tạo PowerPoint đẹp, chuyên nghiệp — hỗ trợ font tiếng Việt (PptxGenJS)
  prompt-engineering/        # Prompt engineering patterns, agent prompting best practices, persuasion principles cho LLM interaction
  prompt-generator/          # Meta-prompting — tạo prompt chất lượng cao
  prompt-generator-v2/       # KERNEL framework — prompt engineering nâng cao
  sequential-thinking/       # Phân tích từng bước cho vấn đề phức tạp — revision, branching, hypothesis
  skill-auto-improver/       # Phân tích và cải tiến skill tự động — quality audit + improvement patterns
  social-post/               # Viết bài social đa platform (Facebook, Threads, LinkedIn, Zalo) chia sẻ góc nhìn chiều sâu — anti-AI rules, self-critique
  speech-to-text/            # Chuyển file audio/video thành text kèm timestamps qua Soniox API — hỗ trợ 60+ ngôn ngữ, audio (mp3/wav/flac) + video (mp4/mov/mkv/avi)
  style-writer/              # Skill viết lách hợp nhất — 2 workflow: Writer (mặc định, viết nội dung theo voice + structure) + Analyze (bóc tách DNA văn phong → tạo voice mới). Gồm voices (7 loại) + structures (8 loại)
  substack-tools/            # Quản lý bài viết Substack: draft, schedule, publish, list, sections + scan/crawl newsletter khác
  systems-thinking/          # Phân tích tư duy hệ thống theo framework Donella Meadows (Thinking in Systems)
  things-manager/            # Things 3 task management via things-cli (Go CLI)
  van-tu-tu-training/        # Xây dựng tài liệu training theo mô hình Văn-Tư-Tu (Tam Tuệ Học) — kiến trúc modular, templates đầy đủ
  wisdom-mentor/             # Trò chuyện với người thầy tri thức (28 mentors)
  work-explainer/            # Personal teacher — giải thích công việc đã làm (9-step framework)
  workshop-builder/          # Thiết kế workshop theo Backwards Design + 4Cs + Kirkpatrick
  youtube-title-generator/   # Tạo tiêu đề YouTube hấp dẫn
  youtube-transcript/        # Tải transcript (phụ đề/captions) từ YouTube video qua yt-dlp, convert VTT sang plain text
agents/                      # Các agent definitions (planned)
hooks/                       # Các hook scripts (planned)
mcp/                         # Các MCP server configs (planned)
```

## Skill Structure

Mỗi skill là một thư mục trong `skills/`. Cấu trúc chuẩn:

```
skills/<skill-name>/
  SKILL.md                   # [BẮT BUỘC] Prompt chính — load khi skill được gọi
  references/                # [Tùy chọn] Tài liệu tham khảo, rules, examples
  scripts/                   # [Tùy chọn] Shell/Python scripts thực thi
  templates/                 # [Tùy chọn] Templates cho output
```

**Quy tắc path quan trọng cho AI:**

- **Entry point**: Luôn là `skills/<skill-name>/SKILL.md` — đây là file duy nhất được load tự động khi skill được gọi.
- **References**: Nằm trong `skills/<skill-name>/references/` — SKILL.md reference đến các file này, AI load khi cần tra cứu.
- **Scripts**: Nằm trong `skills/<skill-name>/scripts/` — các script thực thi (shell, python). Chạy từ thư mục gốc project.
- **Templates**: Nằm trong `skills/<skill-name>/templates/` — template cho output format.
- **KHÔNG** dùng `docs/` làm subdirectory trong skill (dùng `references/` thay thế).

### Chi tiết từng skill

| Skill                      | Subdirectories                                                       | Ghi chú                                                                                                                                                                                                                              |
| -------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ai-artist`                | `references/` `scripts/` `data/`                                     | nano-banana, image-prompting, validation-workflow, domain guides, awesome-prompts.csv, styles/techniques/lighting CSVs                                                                                                               |
| `anti-ai-writing`          | —                                                                    | Chỉ có SKILL.md (rule chung viết tiếng Việt không giống AI)                                                                                                                                                                          |
| `codex-image`              | `scripts/` `references/`                                             | Tạo ảnh qua Codex CLI (gpt-image-2). remove-chroma-key.py, batch-generate.py, prompt-guide, size-guide                                                                                                                              |
| `creative-thought-partner` | —                                                                    | Chỉ có SKILL.md                                                                                                                                                                                                                      |
| `deep-insight`             | `references/`                                                        | framework-foundation, observation-guide, analysis-patterns, synthesis-methods                                                                                                                                                        |
| `deep-learner`             | `references/` `templates/`                                           | easy-explain-guide, long-content-strategy, note-structure, output-template                                                                                                                                                           |
| `deep-reader`              | —                                                                    | Chỉ có SKILL.md. 10 command phân tích đa chiều: summary, explain, insights, map, critique, article, script, questions, checklist, gaps                                                                                               |
| `facebook`                 | `scripts/` `references/`                                             | fb-post.sh, snap-helpers.py, tag-search.py. Hỗ trợ text + ảnh (multi-image) + tag friends                                                                                                                                           |
| `game-theory-lens`         | `references/` `templates/`                                           | core-concepts, strategic-games, information-signaling, repeated-games-trust, mechanism-design, evolution-cooperation, bargaining-coalitions, paradoxes-fallacies, analysis-output                                                    |
| `ghost-blog`               | `scripts/`                                                           | Python scripts + tests cho Ghost CMS API                                                                                                                                                                                             |
| `meeting-minutes`          | `references/`                                                        | minutes-schema, insights-patterns. 2 workflow: Minutes (biên bản) + Insights (phân tích giao tiếp)                                                                                                                                   |
| `outline-writer`           | `references/`                                                        | content-map-rules, detail-levels, framework-mapping, outline-structure, report-format. Outline thuần nội dung (sequence of sections), không quyết định media, không quy định cách viết/tone/style                                     |
| `pexels-media`             | —                                                                    | Chỉ có SKILL.md. Source ảnh/video royalty-free từ Pexels API (search, curated, popular, collections). Download multi-resolution + sidecar metadata (.meta.json) bắt buộc cho mỗi file                                                |
| `pinchtab`                 | `references/`                                                        | api-reference, cli-reference, workflow-patterns                                                                                                                                                                                      |
| `planning-content`         | `references/` `scripts/`                                             | Phân tích input → convert (PDF/DOCX/EPUB/URL/YouTube) → research → outline ý chính. Detail levels, tier processing cho tài liệu lớn (Standard/<50K, Tier 2/50-100K, Tier 3/>=100K). Batch + content map + coverage check. KHÔNG can thiệp cách viết/tone/style |
| `problem-solving`          | `references/`                                                        | collision-zone-thinking, inversion-exercise, meta-pattern-recognition, scale-game, simplification-cascades, when-stuck                                                                                                               |
| `pptx-creator`             | `references/` `scripts/`                                             | design-system, slide-types, pptxgenjs-api, compile.js                                                                                                                                                                                |
| `prompt-engineering`       | —                                                                    | Chỉ có SKILL.md. Few-shot, chain-of-thought, template systems, system prompt design, agent prompting, persuasion principles                                                                                                         |
| `prompt-generator`         | —                                                                    | Chỉ có SKILL.md                                                                                                                                                                                                                      |
| `prompt-generator-v2`      | —                                                                    | Chỉ có SKILL.md                                                                                                                                                                                                                      |
| `sequential-thinking`      | `references/` `scripts/` `tests/`                                    | core-patterns, examples (api/debug/architecture), advanced-techniques, advanced-strategies, process-thought.js, format-thought.js                                                                                                    |
| `skill-auto-improver`      | `references/`                                                        | quality-checklist, improvement-patterns                                                                                                                                                                                              |
| `social-post`              | `references/`                                                        | craft-techniques, anti-ai-rules, example-output                                                                                                                                                                                      |
| `speech-to-text`           | `references/` `scripts/`                                             | Soniox async API, transcribe.js (Node.js), audio + video (ffmpeg extract), output timestamps/text/SRT, 60+ ngôn ngữ                                                                                                                 |
| `style-writer`             | `references/voices/` `references/structures/`                        | voices (7 voice generic, có thể thêm voice analyzed từ corpus), structures (8 loại), analysis-dimensions, anti-patterns, output-template. Workflow Writer (mặc định) + Analyze (output → voices/)                                    |
| `substack-tools`           | `references/` `scripts/`                                             | substack_cli.py, substack_crawl.py, api-quirks, batch-operations, crawl-guide                                                                                                                                                        |
| `systems-thinking`         | `references/` `templates/`                                           | system-traps, leverage-points, systems-wisdom, analysis-output                                                                                                                                                                       |
| `things-manager`           | —                                                                    | Chỉ có SKILL.md                                                                                                                                                                                                                      |
| `van-tu-tu-training`       | `references/`                                                        | naming-convention, philosophy-foundation, modular-architecture, ratio-adjustment, gdocs-compatibility, template-training-brief, template-van, template-tu-suy-tu, template-tu-thuc-hanh, template-danh-gia, template-facilitator-hub |
| `wisdom-mentor`            | `references/`                                                        | 28 mentor profiles (mỗi mentor 1 file .md)                                                                                                                                                                                           |
| `work-explainer`           | —                                                                    | Chỉ có SKILL.md                                                                                                                                                                                                                      |
| `workshop-builder`         | `references/`                                                        | frameworks, activity-library, templates, example-walkthrough, prepare-deliver-followup                                                                                                                                               |
| `youtube-title-generator`  | `references/`                                                        | title-examples                                                                                                                                                                                                                       |
| `youtube-transcript`       | `references/` `scripts/`                                             | Tải transcript YouTube qua yt-dlp. vtt-to-txt.py (convert/dedup), whisper-guide, error-handling                                                                                                                                      |


## Installation

```bash
claude plugin install gh:hoangvantuan/shun-claude-plugin
```

## Development Workflow

### Tạo skill mới

Luôn sử dụng `/skill-creator` để bắt đầu tạo skill mới. Skill creator sẽ hướng dẫn cấu trúc chuẩn và tạo các file cần thiết (SKILL.md, prompt, scripts).

### Development Principles

- **YAGNI/KISS/DRY** - Minimal, focused implementations
- **kebab-case** file naming with descriptive names
- **<200 lines** per code file
- Mỗi skill/agent/hook/mcp là một thư mục độc lập trong folder tương ứng

### Auto-update Documentation

Khi thêm, xóa, hoặc đổi tên bất kỳ tính năng nào (skill, agent, mcp, hook), **tự động cập nhật** lại:

- **CLAUDE.md** — cập nhật phần `## Structure` cho đúng cấu trúc hiện tại
- **README.md** — cập nhật danh sách tính năng và mô tả tương ứng

### Single Source of Truth

- Mỗi thông tin chỉ được định nghĩa **một nơi duy nhất**. Không copy nội dung giữa các file — thay vào đó reference đến file gốc.
- CLAUDE.md chỉ chứa rules tổng quan của dự án. Hướng dẫn chi tiết cho từng skill/agent/hook/mcp nằm trong SKILL.md hoặc README riêng của thư mục đó.
- Khi cần hướng dẫn phân nhánh (chi tiết, ví dụ cụ thể, API specs), **tách thành file riêng** và reference bằng đường dẫn. Claude Code sẽ load file khi cần thay vì load hết vào context.

Ví dụ cấu trúc reference:

```
skills/ghost-blog/
  SKILL.md                    # Prompt chính — load khi skill được gọi
  references/api-reference.md # Chi tiết API — load khi cần tra cứu
  references/examples.md      # Ví dụ — load khi cần tham khảo
```
