"""Helper utilities for OpenProject API."""

from __future__ import annotations

import json
from typing import Any, Generator, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .client import OpenProjectClient


def build_filters(filters: list[dict]) -> str:
    """Build filter JSON string for API queries.

    Args:
        filters: List of filter dicts
            Example: [{"status": {"operator": "=", "values": ["1"]}}]

    Returns:
        JSON string for 'filters' query param
    """
    return json.dumps(filters)


def build_sort(sort_by: list[tuple[str, str]]) -> str:
    """Build sortBy JSON string.

    Args:
        sort_by: List of (field, direction) tuples
            Example: [("updated_at", "desc"), ("id", "asc")]

    Returns:
        JSON string for 'sortBy' query param
    """
    return json.dumps([[field, direction] for field, direction in sort_by])


def parse_hal_response(response: dict) -> dict:
    """Parse HAL+JSON response into structured format.

    Args:
        response: Raw HAL+JSON response dict

    Returns:
        Structured dict with type, data, links, embedded
    """
    return {
        "type": response.get("_type"),
        "data": {k: v for k, v in response.items() if not k.startswith("_")},
        "links": response.get("_links", {}),
        "embedded": response.get("_embedded", {})
    }


def paginate(
    client: "OpenProjectClient",
    path: str,
    params: Optional[dict] = None,
    page_size: int = 100
) -> Generator[dict, None, None]:
    """Auto-paginate through collection results.

    Args:
        client: OpenProjectClient instance
        path: API endpoint path
        params: Additional query parameters
        page_size: Items per page (default 100)

    Yields:
        Individual items from the collection
    """
    params = dict(params) if params else {}
    params["pageSize"] = page_size
    offset = 1

    while True:
        params["offset"] = offset
        response = client.get(path, params=params)
        embedded = response.get("_embedded", {})
        elements = embedded.get("elements", [])

        for item in elements:
            yield item

        if len(elements) < page_size:
            break
        offset += 1


def extract_id_from_href(href: str) -> Optional[int]:
    """Extract resource ID from HAL href.

    Args:
        href: HAL href string (e.g., "/api/v3/projects/5")

    Returns:
        Integer ID or None if extraction fails
    """
    if not href:
        return None
    parts = href.rstrip("/").split("/")
    try:
        return int(parts[-1])
    except ValueError:
        return None
