# Development Guide

Hướng dẫn phát triển Skills, Commands, Hooks, và Agents cho Claude Code plugin.

## Prerequisites

```bash
# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

## Components

| Component | Description | Guide |
|-----------|-------------|-------|
| **Skills** | Instructions loaded dynamically for specialized tasks | [skills.md](skills.md) |
| **Commands** | Slash commands (`/fix`, `/plan`, etc.) | [commands.md](commands.md) |
| **Hooks** | Event-triggered scripts (session init, tool calls) | [hooks.md](hooks.md) |
| **Agents** | Specialized subagents for complex tasks | [agents.md](agents.md) |

## Quick Start

```bash
# Clone and setup
git clone gh:shun/claude-plugin
cd claude-plugin

# Create Python environment
uv venv --python 3.11
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dev dependencies
uv pip install pytest httpx
```

## Project Structure

```
shun_claude_plugin/
├── skills/                 # Packaged skills for distribution
│   └── openproject/        # Example: OpenProject API skills
├── commands/               # Root-level commands
├── hooks/                  # Root-level hooks
├── .claude/
│   ├── skills/             # Internal skills
│   ├── commands/           # Internal commands
│   ├── hooks/              # Internal hooks
│   ├── agents/             # Agent definitions
│   └── scripts/            # Helper scripts
├── plugin.json             # Plugin manifest
└── docs/development/       # This guide
```

## Development Principles

- **YAGNI** - You Aren't Gonna Need It
- **KISS** - Keep It Simple, Stupid
- **DRY** - Don't Repeat Yourself
- **<200 lines** per code file
- **kebab-case** file naming

## Testing

```bash
# Run tests for a skill
cd skills/openproject
uv venv && source .venv/bin/activate
uv pip install -r openproject-core/requirements.txt
pytest -v

# Run specific test
pytest -v -k "test_function_name"
```

## Publishing

```bash
# Validate plugin.json
cat plugin.json | python -m json.tool

# Test installation locally
claude plugin install .

# Publish to GitHub
git push origin main
```
