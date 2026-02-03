"""OpenProject Core - API utilities for OpenProject integration."""

from .client import OpenProjectClient, ConnectionStatus, check_connection
from .exceptions import OpenProjectError, AuthenticationError, OpenProjectAPIError
from .helpers import build_filters, build_sort, parse_hal_response, paginate, extract_id_from_href
from .hal_types import HALLink, HALResponse, CollectionResponse, ErrorResponse
from .project_config import (
    init_config,
    load_config,
    load_session_config,
    refresh_config,
    require_config,
    is_config_initialized,
    get_config_path,
    get_project_id,
    get_type_id,
    get_status_id,
    get_priority_id,
    get_version_id,
    get_custom_field_name,
    print_config_summary,
    ProjectConfig,
)

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
    "init_config",
    "load_config",
    "load_session_config",
    "refresh_config",
    "require_config",
    "is_config_initialized",
    "get_config_path",
    "get_project_id",
    "get_type_id",
    "get_status_id",
    "get_priority_id",
    "get_version_id",
    "get_custom_field_name",
    "print_config_summary",
    "ProjectConfig",
]
