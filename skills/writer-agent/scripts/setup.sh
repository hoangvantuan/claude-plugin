#!/bin/bash
# Writer-Agent Skill Setup Script
# Uses uv for fast, reliable Python environment management

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "=== Writer-Agent Setup ==="
echo "Skill directory: $SKILL_DIR"
echo "Virtual env: $VENV_DIR"
echo ""

# Check uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed."
    echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Create virtual environment
echo "[1/3] Creating virtual environment..."
if [ -d "$VENV_DIR" ]; then
    echo "  Existing venv found, removing..."
    rm -rf "$VENV_DIR"
fi
uv venv "$VENV_DIR"

# Install dependencies
echo "[2/3] Installing dependencies..."
uv pip install -r "$SCRIPT_DIR/requirements.txt" --python "$VENV_DIR/bin/python"

# Verify installation
echo "[3/3] Verifying installation..."
"$VENV_DIR/bin/python" -c "import docling; print(f'  Docling version: {docling.__version__}')" 2>/dev/null || {
    echo "  Warning: Docling import failed. Some features may not work."
}

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Available commands:"
echo ""
echo "  # Convert document (PDF, DOCX, etc.)"
echo "  $SCRIPT_DIR/wa-convert /path/to/file.pdf [output_dir]"
echo ""
echo "  # Handle pasted text"
echo "  echo 'content' | $SCRIPT_DIR/wa-paste-text - --title 'Title'"
echo ""
echo "  # Validate coverage report"
echo "  $SCRIPT_DIR/wa-validate docs/generated/book/analysis/_coverage.md"
