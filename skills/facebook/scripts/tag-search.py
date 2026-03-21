#!/usr/bin/env python3
"""
Search tag results from PinchTab snap — prioritize friends over non-friends.
All inputs via environment variables to avoid shell string escaping.

Environment variables:
  SNAP_JSON      - JSON from `pinchtab snap` (stdin if empty)
  TAG_NAME       - friend name to search for
  TAG_ID         - (optional) Facebook ID for precise matching
  FRIEND_KW      - pipe-separated friend keywords (e.g. "bạn bè|friend")
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
    tag_id = os.environ.get("TAG_ID", "")
    tag_name = norm(os.environ.get("TAG_NAME", ""))
    friend_keywords = os.environ.get("FRIEND_KW", "bạn bè|friend").split("|")

    # Mode 1: match by Facebook ID — search ALL string fields of each node
    # Facebook accessibility tree may embed IDs in ref, url, name, description, or other fields
    if tag_id:
        for n in nodes:
            for val in n.values():
                if isinstance(val, str) and tag_id in val:
                    print(n.get("ref", ""))
                    return
        # ID not found — fall through to name-based matching instead of giving up
        if not tag_name:
            return

    # Mode 2: match by name, prioritize friends
    friend_ref = None
    first_ref = None

    for n in nodes:
        name = n.get("name", "")
        desc = n.get("description", "")
        if tag_name in norm(name) or tag_name in norm(desc):
            if first_ref is None:
                first_ref = n.get("ref", "")
            desc_l = desc.lower()
            if any(fk.strip() in desc_l for fk in friend_keywords):
                friend_ref = n.get("ref", "")
                break

    print(friend_ref or first_ref or "")


if __name__ == "__main__":
    main()
