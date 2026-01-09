"""OpenProject Core - API utilities for OpenProject integration."""

from .client import OpenProjectClient
from .exceptions import OpenProjectError, AuthenticationError, OpenProjectAPIError
from .helpers import build_filters, build_sort, parse_hal_response, paginate, extract_id_from_href
from .types import HALLink, HALResponse, CollectionResponse, ErrorResponse

__all__ = [
    "OpenProjectClient",
    "OpenProjectError",
    "AuthenticationError",
    "OpenProjectAPIError",
    "build_filters",
    "build_sort",
    "parse_hal_response",
    "paginate",
    "extract_id_from_href",
    "HALLink",
    "HALResponse",
    "CollectionResponse",
    "ErrorResponse",
]
