# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dự án phát triển các plugin cho Claude Code, bao gồm: **skills**, **agents**, **hooks**, và **MCP servers**. Mỗi plugin mở rộng khả năng của Claude Code cho các workflow chuyên biệt.

## Structure

```
.claude-plugin/plugin.json   # Plugin manifest
skills/                      # Các skill plugins
  openproject/               # OpenProject API v3 integration
  ghost-blog/                # Ghost CMS blog management
  proslide/                  # Professional slide/presentation creation
  writer-agent/              # Document transformation and article writing
  prompt-generator/          # Meta-prompting — tạo prompt chất lượng cao
  viral-post-creator/        # Tạo bài đăng viral trên social media
  youtube-title-generator/   # Tạo tiêu đề YouTube hấp dẫn
  creative-thought-partner/  # Đối tác tư duy sáng tạo — brainstorming
  deep-post-ideas/           # Trích xuất outline bài đăng từ tài liệu
  deep-learner/              # Học hiểu sâu nội dung — tài liệu học có cấu trúc
agents/                      # Các agent definitions (planned)
hooks/                       # Các hook scripts (planned)
mcp/                         # Các MCP server configs (planned)
```

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
skills/openproject/
  SKILL.md              # Prompt chính — load khi skill được gọi
  docs/api-reference.md # Chi tiết API — load khi cần tra cứu
  docs/examples.md      # Ví dụ — load khi cần tham khảo
```
