# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dự án phát triển các plugin cho Claude Code, bao gồm: **skills**, **agents**, **hooks**, và **MCP servers**. Mỗi plugin mở rộng khả năng của Claude Code cho các workflow chuyên biệt.

## Structure

```
.claude-plugin/plugin.json   # Plugin manifest
skills/                      # Các skill plugins (chi tiết xem ## Skill Structure)
  content-planner/           # Content planning & writing cho Facebook + Blog
  creative-thought-partner/  # Đối tác tư duy sáng tạo — brainstorming
  deep-learner/              # Học hiểu sâu nội dung — tài liệu học có cấu trúc
  deep-post-ideas/           # Trích xuất outline bài đăng từ tài liệu
  facebook/                  # Facebook automation via PinchTab (wall post, tag friends)
  ghost-blog/                # Ghost CMS blog management
  outline-writer/            # Content analysis & outline creation (presentation/blog/doc)
  pinchtab/                  # Browser automation for AI agents via PinchTab HTTP API
  prompt-generator/          # Meta-prompting — tạo prompt chất lượng cao
  prompt-generator-v2/       # KERNEL framework — prompt engineering nâng cao
  slidev-builder/            # Slidev presentation builder from outline
  things-manager/            # Things 3 task management via things-cli (Go CLI)
  viral-post-creator/        # Tạo bài đăng viral trên social media
  wisdom-mentor/             # Trò chuyện với người thầy tri thức (28 mentors)
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

| Skill | Subdirectories | Ghi chú |
|-------|---------------|---------|
| `content-planner` | `references/` | blog-types, content-frameworks, facebook-types |
| `creative-thought-partner` | — | Chỉ có SKILL.md |
| `deep-learner` | `templates/` | note-structure, output-template |
| `deep-post-ideas` | `references/` | example-phrasing |
| `facebook` | `scripts/` | fb-post.sh, snap-helpers.py, tag-search.py |
| `ghost-blog` | `scripts/` | Python scripts + tests cho Ghost CMS API |
| `outline-writer` | `references/` | outline-rules |
| `pinchtab` | `references/` | api-reference, cli-reference, workflow-patterns |
| `prompt-generator` | — | Chỉ có SKILL.md |
| `prompt-generator-v2` | — | Chỉ có SKILL.md |
| `slidev-builder` | `references/` | slide-templates |
| `things-manager` | — | Chỉ có SKILL.md |
| `viral-post-creator` | `references/` | example-phrasing |
| `wisdom-mentor` | `references/` | 28 mentor profiles (mỗi mentor 1 file .md) |
| `writer-agent` | `audiences/` `emotional_maps/` `identities/` `meta/` `references/` `scripts/` `structures/` `templates/` `voices/` | Skill phức tạp nhất — có 9 subdirectories |
| `youtube-title-generator` | `references/` | title-examples |

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
