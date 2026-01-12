# Root conftest.py for pytest
import sys
from pathlib import Path

# Ensure all packages are importable
root = Path(__file__).parent
sys.path.insert(0, str(root))
