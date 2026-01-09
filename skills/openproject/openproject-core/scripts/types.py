"""Type definitions for OpenProject API responses."""

from typing import TypedDict, Optional, Any


class HALLink(TypedDict, total=False):
    """HAL link structure."""
    href: str
    title: Optional[str]
    method: Optional[str]
    templated: Optional[bool]


class HALResponse(TypedDict, total=False):
    """Base HAL+JSON response structure."""
    _type: str
    _links: dict[str, HALLink]
    _embedded: dict[str, Any]


class CollectionResponse(HALResponse):
    """Paginated collection response."""
    total: int
    count: int
    pageSize: int
    offset: int


class ErrorResponse(TypedDict):
    """Error response structure."""
    _type: str
    errorIdentifier: str
    message: str
