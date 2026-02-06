# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Code plugin package - provides skills, commands, hooks, and agents for enhanced Claude Code workflows.

## Structure

* `.claude-plugin/plugin.json` - Plugin manifest

* `skills/` - Plugin skills (openproject, ghost-blog, proslide, writer-agent)

## Installation

```bash
claude plugin install gh:hoangvantuan/shun-claude-plugin
```

## Development Principles

* **YAGNI/KISS/DRY** - Minimal, focused implementations

* **kebab-case** file naming with descriptive names

* **<200 lines** per code file

