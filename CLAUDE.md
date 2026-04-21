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
  content-planner/           # Content planning & writing cho Facebook + Blog
  creative-thought-partner/  # Đối tác tư duy sáng tạo — brainstorming
  deep-learner/              # Dẫn dắt từng bước hiểu sâu bản chất nội dung — 4 lớp hiểu + áp dụng đời sống
  deep-post-ideas/           # Trích xuất outline bài đăng từ tài liệu
  facebook/                  # Facebook automation via PinchTab (wall post, tag friends)
  ghost-blog/                # Ghost CMS blog management
  outline-writer/            # Content analysis & outline creation (presentation/blog/doc)
  pinchtab/                  # Browser automation for AI agents via PinchTab HTTP API
  problem-solving/           # Kỹ thuật giải quyết vấn đề có hệ thống — inversion, collision-zone, scale-game
  pptx-creator/              # Tạo PowerPoint đẹp, chuyên nghiệp — hỗ trợ font tiếng Việt (PptxGenJS)
  prompt-generator/          # Meta-prompting — tạo prompt chất lượng cao
  prompt-generator-v2/       # KERNEL framework — prompt engineering nâng cao
  sequential-thinking/       # Phân tích từng bước cho vấn đề phức tạp — revision, branching, hypothesis
  slidev-builder/            # Slidev presentation builder from outline
  social-post/               # Viết bài social đa platform (Facebook, Threads, LinkedIn, Zalo) chia sẻ góc nhìn chiều sâu — 3 archetype, cấu trúc 5 phần, anti-AI rules, self-critique
  style-dna/                 # Bóc tách DNA văn phong từ corpus bài viết → style guide markdown tái sử dụng (8 chiều, signature phrases, công thức tái tạo)
  style-library/             # Thư viện style guide — 3 catalog: personas (Tuấn), archetypes (Patient Observer, Dramatic Prophet, Quiet Devastator), voices (7 voice × 3 variant). Atomic, không load skill khác
  writing-structures/        # Thư viện khung bài — 9 structures (Story Arc, BLUF-Evidence, Building Blocks, Depth-Practice, Five Layers, Master-Student, Spiral Return, Adaptive, Social 5-Parts) + 5 frameworks (PAS, Inverted Pyramid, Step-by-step, SAR, Progressive Disclosure). Atomic
  writing-context/           # Thư viện context dimensions — 3 trục: identities (3), audiences (3), emotions (3). Atomic
  substack-tools/            # Quản lý bài viết Substack: draft, schedule, publish, list, sections + scan/crawl newsletter khác
  things-manager/            # Things 3 task management via things-cli (Go CLI)
  deep-insight/              # Quan sát đa chiều → Phân tích tách lớp → Đúc kết cốt lõi để hiểu sâu vấn đề
  game-theory-lens/          # Phân tích chủ đề qua lăng kính Lý thuyết Trò chơi (Game Theory)
  skill-auto-improver/       # Phân tích và cải tiến skill tự động — quality audit + improvement patterns
  systems-thinking/          # Phân tích tư duy hệ thống theo framework Donella Meadows (Thinking in Systems)
  van-tu-tu-training/        # Xây dựng tài liệu training theo mô hình Văn-Tư-Tu (Tam Tuệ Học)
  viral-post-creator/        # Tạo bài đăng viral trên social media
  wisdom-mentor/             # Trò chuyện với người thầy tri thức (28 mentors)
  work-explainer/            # Personal teacher — giải thích công việc đã làm (9-step framework)
  workshop-builder/          # Thiết kế workshop theo Backwards Design + 4Cs + Kirkpatrick
  writer-agent/              # Document transformation and article writing
  youtube-title-generator/   # Tạo tiêu đề YouTube hấp dẫn
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

| Skill                      | Subdirectories                                                                                                     | Ghi chú                                                                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `ai-artist`                | `references/` `scripts/` `data/`                                                                                   | nano-banana, image-prompting, validation-workflow, domain guides, awesome-prompts.csv, styles/techniques/lighting CSVs                     |
| `anti-ai-writing`          | —                                                                                                                  | Chỉ có SKILL.md (rule chung viết tiếng Việt không giống AI)                                                                               |
| `content-planner`          | `references/`                                                                                                      | blog-types, content-frameworks, facebook-types                                                                                            |
| `creative-thought-partner` | —                                                                                                                  | Chỉ có SKILL.md                                                                                                                           |
| `deep-learner`             | `references/` `templates/`                                                                                         | easy-explain-guide, long-content-strategy, note-structure, output-template                                                                |
| `deep-insight`             | `references/`                                                                                                      | framework-foundation, observation-guide, analysis-patterns, synthesis-methods                                                             |
| `deep-post-ideas`          | `references/`                                                                                                      | example-phrasing                                                                                                                          |
| `game-theory-lens`         | `references/` `templates/`                                                                                         | core-concepts, strategic-games, information-signaling, repeated-games-trust, mechanism-design, evolution-cooperation, bargaining-coalitions, paradoxes-fallacies, analysis-output |
| `facebook`                 | `scripts/`                                                                                                         | fb-post.sh, snap-helpers.py, tag-search.py                                                                                                |
| `ghost-blog`               | `scripts/`                                                                                                         | Python scripts + tests cho Ghost CMS API                                                                                                  |
| `outline-writer`           | `references/`                                                                                                      | outline-rules                                                                                                                             |
| `pinchtab`                 | `references/`                                                                                                      | api-reference, cli-reference, workflow-patterns                                                                                           |
| `problem-solving`          | `references/`                                                                                                      | collision-zone-thinking, inversion-exercise, meta-pattern-recognition, scale-game, simplification-cascades, when-stuck                    |
| `pptx-creator`             | `references/` `scripts/`                                                                                           | design-system, slide-types, pptxgenjs-api, compile.js                                                                                     |
| `prompt-generator`         | —                                                                                                                  | Chỉ có SKILL.md                                                                                                                           |
| `prompt-generator-v2`      | —                                                                                                                  | Chỉ có SKILL.md                                                                                                                           |
| `sequential-thinking`      | `references/` `scripts/` `tests/`                                                                                  | core-patterns, examples (api/debug/architecture), advanced-techniques, advanced-strategies, process-thought.js, format-thought.js          |
| `skill-auto-improver`      | `references/`                                                                                                      | quality-checklist, improvement-patterns                                                                                                   |
| `slidev-builder`           | `references/`                                                                                                      | slide-templates                                                                                                                           |
| `social-post`              | `references/`                                                                                                      | archetypes (Patient Observer, Dramatic Prophet, Quiet Devastator), craft-techniques, anti-ai-rules, example-output                        |
| `style-dna`                | `references/`                                                                                                      | analysis-dimensions (8 chiều chi tiết), output-template (khung markdown chuẩn), anti-patterns (lỗi cần tránh)                             |
| `style-library`            | `references/personas/` `references/archetypes/` `references/voices/`                                              | 3 catalog atomic: personas (tuan), archetypes (patient-observer, dramatic-prophet, quiet-devastator), voices (7 voice × 3 variant main/compact/exemplars = 21 file). Độc lập, không load skill khác |
| `writing-structures`       | `references/structures/` `references/frameworks.md`                                                                | 9 structures (story-arc, bluf-evidence, building-blocks, depth-practice, five-layers, master-student, spiral-return, adaptive, social-5-parts; mỗi structure có main + compact variant) + 5 frameworks (PAS, Inverted Pyramid, Step-by-step, SAR, Progressive Disclosure). Độc lập |
| `writing-context`          | `references/identities/` `references/audiences/` `references/emotions/`                                            | 3 trục atomic: identities (contemplative-thinker, knowledge-curator, tech-builder), audiences (busy-professionals, curious-beginners, deep-seekers), emotions (empower-challenge, provoke-transform, reflect-discover). Độc lập |
| `systems-thinking`         | `references/` `templates/`                                                                                         | system-traps, leverage-points, systems-wisdom, analysis-output                                                                            |
| `substack-tools`           | `references/` `scripts/`                                                                                           | substack_cli.py, substack_crawl.py, api-quirks, batch-operations, crawl-guide                                                             |
| `things-manager`           | —                                                                                                                  | Chỉ có SKILL.md                                                                                                                           |
| `van-tu-tu-training`       | `references/`                                                                                                      | naming-convention, philosophy-foundation, modular-architecture, ratio-adjustment, gdocs-compatibility, template-van, template-tu-suy-tu, template-tu-thuc-hanh, template-danh-gia, template-facilitator-hub |
| `viral-post-creator`       | `references/`                                                                                                      | example-phrasing                                                                                                                          |
| `wisdom-mentor`            | `references/`                                                                                                      | 28 mentor profiles (mỗi mentor 1 file .md)                                                                                                |
| `work-explainer`           | —                                                                                                                  | Chỉ có SKILL.md                                                                                                                           |
| `workshop-builder`         | `references/`                                                                                                      | frameworks, activity-library, templates, example-walkthrough, prepare-deliver-followup                                                    |
| `writer-agent`             | `audiences/` `emotional_maps/` `identities/` `meta/` `references/` `scripts/` `structures/` `templates/` `voices/` | Skill phức tạp nhất — có 9 subdirectories                                                                                                 |
| `youtube-title-generator`  | `references/`                                                                                                      | title-examples                                                                                                                            |


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
