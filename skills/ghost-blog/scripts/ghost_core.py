#!/usr/bin/env python3
"""Ghost Admin API core module - auth, HTTP client, pagination, utilities.

Provides JWT authentication, HTTP client with retry logic, pagination helper,
and utility functions for Ghost Admin API integration.

Environment Variables:
    GHOST_URL: Ghost blog URL (e.g., https://blog.example.com)
    GHOST_ADMIN_KEY: Admin API key in id:secret format
    GHOST_API_VERSION: API version (default: v5.0)
"""

import os
import time
from binascii import unhexlify
from pathlib import Path
from typing import Any, Dict, Generator, Optional, Tuple

import jwt
import requests
from dotenv import load_dotenv

# Load .env from scripts directory
_env_path = Path(__file__).parent / '.env'
load_dotenv(_env_path)

# Constants
TOKEN_EXPIRY_SECONDS = 300  # JWT token lifetime (5 minutes)
TOKEN_CACHE_SECONDS = 240   # Cache window (4 minutes, safe margin)
REQUEST_TIMEOUT = 30        # HTTP request timeout in seconds
MAX_RETRIES = 3             # Max retry attempts for transient errors
RETRY_BACKOFF = 1.0         # Initial backoff seconds for retry
ERROR_TRUNCATE_LENGTH = 200 # Max chars for error message truncation


class _TokenCache:
    """Encapsulated token cache to avoid global state mutation issues."""
    def __init__(self):
        self.token: Optional[str] = None
        self.expiry: float = 0

    def get(self, api_key: str) -> str:
        """Get cached token or generate new one."""
        if self.token and self.expiry > time.time():
            return self.token
        self.token = generate_token(api_key)
        self.expiry = time.time() + TOKEN_CACHE_SECONDS
        return self.token

    def clear(self):
        """Clear cached token (useful for testing)."""
        self.token = None
        self.expiry = 0


_token_cache = _TokenCache()


class GhostAPIError(Exception):
    """Custom exception for Ghost API errors.

    Attributes:
        message: Error description
        error_type: Ghost error type (e.g., ValidationError, NotFoundError)
        status_code: HTTP status code
    """
    def __init__(self, message: str, error_type: Optional[str] = None,
                 status_code: Optional[int] = None):
        self.message = message
        self.error_type = error_type
        self.status_code = status_code
        super().__init__(self.message)


def load_config() -> Dict[str, str]:
    """Load Ghost API configuration from environment.

    Returns:
        Dict with keys: ghost_url, admin_key, api_version
    """
    return {
        'ghost_url': os.environ.get('GHOST_URL', '').rstrip('/'),
        'admin_key': os.environ.get('GHOST_ADMIN_KEY', ''),
        'api_version': os.environ.get('GHOST_API_VERSION', 'v5.0')
    }


def validate_config(config: Dict[str, str]) -> Tuple[bool, str]:
    """Validate configuration.

    Args:
        config: Configuration dict from load_config()

    Returns:
        Tuple of (is_valid, error_message). error_message empty if valid.
    """
    if not config['ghost_url']:
        return False, "GHOST_URL not set"
    if not config['admin_key']:
        return False, "GHOST_ADMIN_KEY not set"
    if ':' not in config['admin_key']:
        return False, "GHOST_ADMIN_KEY invalid format (expected id:secret)"
    return True, ""


def generate_token(api_key: str) -> str:
    """Generate JWT token for Ghost Admin API.

    Args:
        api_key: Admin API key in id:secret format

    Returns:
        JWT token string

    Raises:
        ValueError: If api_key format is invalid
    """
    key_id, secret = api_key.split(':')
    iat = int(time.time())
    header = {'alg': 'HS256', 'typ': 'JWT', 'kid': key_id}
    payload = {'iat': iat, 'exp': iat + TOKEN_EXPIRY_SECONDS, 'aud': '/admin/'}
    return jwt.encode(payload, unhexlify(secret), algorithm='HS256', headers=header)


def get_valid_token(api_key: str) -> str:
    """Get cached token or generate new one.

    Uses 4-minute cache window for 5-minute token expiry to ensure
    tokens are always valid during request execution.

    Args:
        api_key: Admin API key in id:secret format

    Returns:
        Valid JWT token string
    """
    return _token_cache.get(api_key)


def api_request(method: str, endpoint: str, data: Optional[Dict] = None,
                params: Optional[Dict] = None, config: Optional[Dict] = None,
                timeout: int = REQUEST_TIMEOUT) -> Dict[str, Any]:
    """Make authenticated request to Ghost Admin API with retry logic.

    Automatically retries on 429 (rate limit) and 5xx (server errors)
    with exponential backoff.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path (e.g., 'posts/')
        data: Request body for POST/PUT
        params: Query parameters
        config: Optional config dict, loads from env if None
        timeout: Request timeout in seconds

    Returns:
        Parsed JSON response dict

    Raises:
        GhostAPIError: On API errors or invalid configuration
    """
    if config is None:
        config = load_config()
    valid, error = validate_config(config)
    if not valid:
        raise GhostAPIError(error, 'ConfigurationError')

    url = f"{config['ghost_url']}/ghost/api/admin/{endpoint.lstrip('/')}"
    token = get_valid_token(config['admin_key'])
    headers = {
        'Authorization': f'Ghost {token}',
        'Accept-Version': config['api_version'],
        'Content-Type': 'application/json'
    }

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.request(
                method, url, headers=headers, json=data, params=params, timeout=timeout
            )
            # Retry on rate limit or server errors
            if response.status_code == 429 or response.status_code >= 500:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_BACKOFF * (2 ** attempt))
                    continue
            return _handle_response(response)
        except requests.RequestException as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFF * (2 ** attempt))
                continue
            raise GhostAPIError(f"Request failed: {str(e)}", 'NetworkError')

    raise GhostAPIError(f"Request failed after {MAX_RETRIES} retries: {last_error}", 'NetworkError')


def _handle_response(response: requests.Response) -> Dict[str, Any]:
    """Parse response and raise on error.

    Args:
        response: requests.Response object

    Returns:
        Parsed JSON dict, or {'success': True} for 204 responses

    Raises:
        GhostAPIError: On API errors or invalid JSON
    """
    if response.status_code == 204:
        return {'success': True}
    try:
        data = response.json()
    except ValueError:
        text_preview = response.text[:ERROR_TRUNCATE_LENGTH]
        if len(response.text) > ERROR_TRUNCATE_LENGTH:
            text_preview += '...'
        raise GhostAPIError(
            f"Invalid JSON response: {text_preview}",
            'ParseError',
            response.status_code
        )
    if 'errors' in data:
        err = data['errors'][0]
        raise GhostAPIError(
            err.get('message', 'Unknown error'),
            err.get('errorType'),
            response.status_code
        )
    return data


def paginate(endpoint: str, params: Optional[Dict] = None,
             config: Optional[Dict] = None) -> Generator[Dict[str, Any], None, None]:
    """Paginate through all results from an endpoint.

    Yields each page response. Caller should extract items from response.

    Args:
        endpoint: API endpoint path
        params: Query parameters (copied, not mutated)
        config: Optional config dict

    Yields:
        Dict containing page data and meta.pagination info
    """
    params = dict(params) if params else {}
    params.setdefault('page', 1)
    params.setdefault('limit', 50)
    while True:
        response = api_request('GET', endpoint, params=params, config=config)
        yield response
        pagination = response.get('meta', {}).get('pagination', {})
        if pagination.get('next') is None:
            break
        params['page'] = pagination['next']


def format_error(error: GhostAPIError, verbose: bool = False) -> str:
    """Format GhostAPIError for CLI output.

    Args:
        error: GhostAPIError instance
        verbose: If True, include all available details

    Returns:
        Formatted error string with type and status code if available
    """
    if verbose:
        parts = []
        if error.error_type:
            parts.append(f"Type: {error.error_type}")
        parts.append(f"Message: {error.message}")
        if error.status_code:
            parts.append(f"HTTP Status: {error.status_code}")
        return " | ".join(parts)

    msg = f"Error: {error.message}"
    if error.error_type:
        msg = f"[{error.error_type}] {msg}"
    if error.status_code:
        msg += f" (HTTP {error.status_code})"
    return msg


def mask_api_key(api_key: str) -> str:
    """Mask API key for safe logging.

    Args:
        api_key: API key string

    Returns:
        Masked key showing only first/last 4 chars of secret
    """
    if ':' in api_key:
        key_id, secret = api_key.split(':')
        if len(secret) > 8:
            return f"{key_id}:{secret[:4]}...{secret[-4:]}"
        return f"{key_id}:***"
    return api_key[:8] + '...' if len(api_key) > 8 else '***'


def main() -> int:
    """CLI entrypoint for connection testing.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    config = load_config()
    valid, error = validate_config(config)
    if not valid:
        print(f"Configuration Error: {error}")
        return 1
    print(f"Ghost URL: {config['ghost_url']}")
    print(f"API Key: {mask_api_key(config['admin_key'])}")
    try:
        response = api_request('GET', 'posts/', params={'limit': 1})
        total = response.get('meta', {}).get('pagination', {}).get('total', 0)
        print(f"Connection successful! Total posts: {total}")
        return 0
    except GhostAPIError as e:
        print(format_error(e))
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
