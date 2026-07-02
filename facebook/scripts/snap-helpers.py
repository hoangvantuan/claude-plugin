#!/usr/bin/env python3
"""
PinchTab snap helpers — find UI elements by role & keywords.
All inputs via environment variables to avoid shell string escaping issues.

Environment variables:
  SNAP_JSON   - JSON string from `pinchtab snap` (stdin if empty)
  SNAP_ROLE   - element role to search for (e.g. "button", "textbox")
  SNAP_KW     - pipe-separated keywords (e.g. "nghĩ gì|what's on your mind")
  SNAP_MODE   - "multi" (substring match, default) or "exact" (exact match)
  SNAP_FIELD  - "ref" (default) or "name" — what to print on match
"""
import json
import os
import sys
import unicodedata


def norm(s: str) -> str:
    return unicodedata.normalize("NFD", s.lower()).strip()


def main():
    raw = os.environ.get("SNAP_JSON", "")
    if not raw:
        raw = sys.stdin.read()

    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        sys.exit(1)

    nodes = data.get("nodes", [])
    role = os.environ.get("SNAP_ROLE", "")
    keywords = os.environ.get("SNAP_KW", "").split("|")
    mode = os.environ.get("SNAP_MODE", "multi")
    field = os.environ.get("SNAP_FIELD", "ref")

    for kw in keywords:
        kw_n = norm(kw.strip())
        if not kw_n:
            continue
        for n in nodes:
            if role and n.get("role") != role:
                continue
            name_n = norm(n.get("name", ""))
            if mode == "exact":
                if name_n == kw_n:
                    print(n.get(field, n.get("ref", "")))
                    return
            else:
                if kw_n in name_n:
                    print(n.get(field, n.get("ref", "")))
                    return


if __name__ == "__main__":
    main()
