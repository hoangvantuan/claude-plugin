#!/bin/bash
# Shared venv setup for wa-* wrapper scripts.
# Usage: source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_wa-common.sh"

# BASH_SOURCE[0] = this file (_wa-common.sh), resolve from its own location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Virtual environment not found."
    echo "Run setup first: $SCRIPT_DIR/setup.sh"
    exit 1
fi
