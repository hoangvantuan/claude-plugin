"""Work package relations."""

import sys
from pathlib import Path
from typing import Iterator, Optional

# Add openproject-core scripts to path
_core_scripts = Path(__file__).parent.parent.parent / "openproject-core" / "scripts"
sys.path.insert(0, str(_core_scripts))

from client import OpenProjectClient
from helpers import paginate

# Valid relation types
RELATION_TYPES = [
    "relates", "duplicates", "duplicated",
    "blocks", "blocked", "precedes", "follows",
    "includes", "partof", "requires", "required"
]


def get_client() -> OpenProjectClient:
    """Get configured client instance."""
    return OpenProjectClient()


def list_relations(wp_id: int) -> Iterator[dict]:
    """List relations for work package.

    Yields:
        Relation dicts
    """
    with get_client() as client:
        yield from paginate(client, f"/work_packages/{wp_id}/relations")


def create_relation(
    from_id: int,
    to_id: int,
    relation_type: str,
    description: Optional[str] = None,
    delay: Optional[int] = None
) -> dict:
    """Create relation between work packages.

    Args:
        from_id: Source work package ID
        to_id: Target work package ID
        relation_type: Type of relation (relates, blocks, follows, etc.)
        description: Optional description
        delay: Days delay (for precedes/follows)

    Returns:
        Created relation dict
    """
    if relation_type not in RELATION_TYPES:
        raise ValueError(f"Invalid relation type: {relation_type}. Valid types: {RELATION_TYPES}")

    data = {
        "_links": {
            "from": {"href": f"/work_packages/{from_id}"},
            "to": {"href": f"/work_packages/{to_id}"}
        },
        "type": relation_type
    }

    if description:
        data["description"] = description
    if delay is not None:
        data["delay"] = delay

    with get_client() as client:
        return client.post("/relations", data)


def delete_relation(relation_id: int) -> dict:
    """Delete relation."""
    with get_client() as client:
        return client.delete(f"/relations/{relation_id}")


def get_relation(relation_id: int) -> dict:
    """Get single relation."""
    with get_client() as client:
        return client.get(f"/relations/{relation_id}")
