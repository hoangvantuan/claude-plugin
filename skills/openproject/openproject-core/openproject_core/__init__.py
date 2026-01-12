"""OpenProject Core - API utilities for OpenProject integration."""

from .client import OpenProjectClient, ConnectionStatus, check_connection
from .exceptions import OpenProjectError, AuthenticationError, OpenProjectAPIError
from .helpers import build_filters, build_sort, parse_hal_response, paginate, extract_id_from_href
from .hal_types import HALLink, HALResponse, CollectionResponse, ErrorResponse

__all__ = [
    "OpenProjectClient",
    "ConnectionStatus",
    "check_connection",
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
