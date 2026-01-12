"""OpenProject API v3 client with Basic Auth (API Key)."""

import os
from typing import Optional, TypedDict

import httpx

try:
    from .exceptions import OpenProjectAPIError, AuthenticationError
except ImportError:
    from exceptions import OpenProjectAPIError, AuthenticationError


class ConnectionStatus(TypedDict):
    """Connection check result."""
    ok: bool
    url: str
    user: Optional[str]
    login: Optional[str]
    email: Optional[str]
    admin: Optional[bool]
    error: Optional[str]


class OpenProjectClient:
    """HTTP client for OpenProject API v3."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 30.0
    ):
        """Initialize OpenProject client.

        Args:
            base_url: OpenProject instance URL (or OPENPROJECT_URL env var)
            api_key: API key for authentication (or OPENPROJECT_API_KEY env var)
            timeout: Request timeout in seconds (default 30.0)

        Raises:
            ValueError: If base_url is not provided
            AuthenticationError: If api_key is not provided
        """
        self.base_url = (base_url or os.getenv("OPENPROJECT_URL", "")).rstrip("/")
        self.api_key = api_key or os.getenv("OPENPROJECT_API_KEY", "")

        if not self.base_url:
            raise ValueError("OPENPROJECT_URL required")
        if not self.api_key:
            raise AuthenticationError("OPENPROJECT_API_KEY required")

        self.client = httpx.Client(
            base_url=f"{self.base_url}/api/v3",
            auth=("apikey", self.api_key),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/hal+json"
            },
            timeout=timeout
        )

    def _handle_response(self, response: httpx.Response) -> dict:
        """Handle API response, raise on errors.

        Args:
            response: httpx Response object

        Returns:
            Parsed JSON response

        Raises:
            AuthenticationError: If 401 response
            OpenProjectAPIError: If 4xx/5xx response
        """
        if response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        if response.status_code >= 400:
            try:
                error_data = response.json() if response.content else {}
            except ValueError:
                error_data = {}
            raise OpenProjectAPIError(
                status_code=response.status_code,
                message=error_data.get("message", "Unknown error"),
                error_id=error_data.get("errorIdentifier")
            )
        try:
            return response.json() if response.content else {}
        except ValueError:
            return {}

    def get(self, path: str, params: Optional[dict] = None) -> dict:
        """GET request.

        Args:
            path: API endpoint path
            params: Query parameters

        Returns:
            Parsed JSON response
        """
        response = self.client.get(path, params=params)
        return self._handle_response(response)

    def post(self, path: str, data: Optional[dict] = None) -> dict:
        """POST request.

        Args:
            path: API endpoint path
            data: Request body data

        Returns:
            Parsed JSON response
        """
        response = self.client.post(path, json=data)
        return self._handle_response(response)

    def patch(self, path: str, data: Optional[dict] = None) -> dict:
        """PATCH request.

        Args:
            path: API endpoint path
            data: Request body data

        Returns:
            Parsed JSON response
        """
        response = self.client.patch(path, json=data)
        return self._handle_response(response)

    def delete(self, path: str) -> dict:
        """DELETE request.

        Args:
            path: API endpoint path

        Returns:
            Parsed JSON response (usually empty)
        """
        response = self.client.delete(path)
        return self._handle_response(response)

    def close(self):
        """Close client connection."""
        self.client.close()

    def check_connection(self) -> ConnectionStatus:
        """Check connection to OpenProject API.

        Returns:
            ConnectionStatus dict with ok, url, user info, and error if any.
        """
        try:
            me = self.get("/users/me")
            return ConnectionStatus(
                ok=True,
                url=self.base_url,
                user=f"{me.get('firstName', '')} {me.get('lastName', '')}".strip(),
                login=me.get("login"),
                email=me.get("email"),
                admin=me.get("admin", False),
                error=None
            )
        except (AuthenticationError, OpenProjectAPIError) as e:
            return ConnectionStatus(
                ok=False,
                url=self.base_url,
                user=None,
                login=None,
                email=None,
                admin=None,
                error=str(e)
            )

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, *args):
        """Context manager exit."""
        self.close()


def check_connection(
    base_url: Optional[str] = None,
    api_key: Optional[str] = None
) -> ConnectionStatus:
    """Check connection to OpenProject API (standalone function).

    Args:
        base_url: OpenProject instance URL (or OPENPROJECT_URL env var)
        api_key: API key for authentication (or OPENPROJECT_API_KEY env var)

    Returns:
        ConnectionStatus dict with ok, url, user info, and error if any.
    """
    try:
        with OpenProjectClient(base_url=base_url, api_key=api_key) as client:
            return client.check_connection()
    except (ValueError, AuthenticationError) as e:
        return ConnectionStatus(
            ok=False,
            url=base_url or os.getenv("OPENPROJECT_URL", ""),
            user=None,
            login=None,
            email=None,
            admin=None,
            error=str(e)
        )
