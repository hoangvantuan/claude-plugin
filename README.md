# Shun Claude Plugin

A collection of skills, commands, hooks, and agents for Claude Code.

## Installation

```bash
claude plugin install gh:shun/claude-plugin
```

## Contents

### Skills

| Skill         | Description                                | Docs                                   |
| ------------- | ------------------------------------------ | -------------------------------------- |
| `openproject` | OpenProject API v3 integration (9 modules) | [README](skills/openproject/README.md) |

### Commands

Coming soon.

### Hooks

Coming soon.

## Development

See each skill's README for setup instructions.

### Run Tests

```bash
# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup and run tests for a skill
cd skills/openproject
uv venv --python 3.9 && source .venv/bin/activate
uv pip install -r openproject-core/requirements.txt
pytest -v
```

## License

MIT
