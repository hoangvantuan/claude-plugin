"""Tests for OpenProject client."""

import pytest
from pytest_httpx import HTTPXMock

import sys
from pathlib import Path

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from client import OpenProjectClient
from exceptions import AuthenticationError, OpenProjectAPIError


class TestClientInit:
    """Tests for client initialization."""

    def test_client_requires_url(self, monkeypatch):
        """Client raises ValueError when URL is missing."""
        monkeypatch.delenv("OPENPROJECT_URL", raising=False)
        monkeypatch.delenv("OPENPROJECT_API_KEY", raising=False)
        with pytest.raises(ValueError, match="OPENPROJECT_URL required"):
            OpenProjectClient(base_url="", api_key="test")

    def test_client_requires_api_key(self, monkeypatch):
        """Client raises AuthenticationError when API key is missing."""
        monkeypatch.delenv("OPENPROJECT_URL", raising=False)
        monkeypatch.delenv("OPENPROJECT_API_KEY", raising=False)
        with pytest.raises(AuthenticationError, match="OPENPROJECT_API_KEY required"):
            OpenProjectClient(base_url="https://test.com", api_key="")

    def test_client_init_with_params(self, monkeypatch):
        """Client initializes with explicit parameters."""
        monkeypatch.delenv("OPENPROJECT_URL", raising=False)
        monkeypatch.delenv("OPENPROJECT_API_KEY", raising=False)
        client = OpenProjectClient(base_url="https://test.com", api_key="testkey")
        assert client.base_url == "https://test.com"
        assert client.api_key == "testkey"
        client.close()

    def test_client_init_from_env(self, monkeypatch):
        """Client initializes from environment variables."""
        monkeypatch.setenv("OPENPROJECT_URL", "https://env.com")
        monkeypatch.setenv("OPENPROJECT_API_KEY", "envkey")
        client = OpenProjectClient()
        assert client.base_url == "https://env.com"
        assert client.api_key == "envkey"
        client.close()

    def test_client_strips_trailing_slash(self, monkeypatch):
        """Client strips trailing slash from URL."""
        monkeypatch.delenv("OPENPROJECT_URL", raising=False)
        monkeypatch.delenv("OPENPROJECT_API_KEY", raising=False)
        client = OpenProjectClient(base_url="https://test.com/", api_key="testkey")
        assert client.base_url == "https://test.com"
        client.close()


class TestClientRequests:
    """Tests for client HTTP methods."""

    @pytest.fixture
    def client(self, monkeypatch):
        """Create test client."""
        monkeypatch.delenv("OPENPROJECT_URL", raising=False)
        monkeypatch.delenv("OPENPROJECT_API_KEY", raising=False)
        c = OpenProjectClient(base_url="https://test.com", api_key="testkey")
        yield c
        c.close()

    def test_get_request(self, client, httpx_mock: HTTPXMock):
        """GET request returns parsed JSON."""
        httpx_mock.add_response(
            url="https://test.com/api/v3/projects",
            json={"_type": "Collection", "total": 1}
        )
        result = client.get("/projects")
        assert result["_type"] == "Collection"
        assert result["total"] == 1

    def test_post_request(self, client, httpx_mock: HTTPXMock):
        """POST request sends JSON and returns parsed response."""
        httpx_mock.add_response(
            url="https://test.com/api/v3/work_packages",
            json={"_type": "WorkPackage", "id": 1}
        )
        result = client.post("/work_packages", data={"subject": "Test"})
        assert result["_type"] == "WorkPackage"
        assert result["id"] == 1

    def test_patch_request(self, client, httpx_mock: HTTPXMock):
        """PATCH request sends JSON and returns parsed response."""
        httpx_mock.add_response(
            url="https://test.com/api/v3/work_packages/1",
            json={"_type": "WorkPackage", "id": 1, "subject": "Updated"}
        )
        result = client.patch("/work_packages/1", data={"subject": "Updated"})
        assert result["subject"] == "Updated"

    def test_delete_request(self, client, httpx_mock: HTTPXMock):
        """DELETE request returns empty or parsed response."""
        httpx_mock.add_response(
            url="https://test.com/api/v3/work_packages/1",
            content=b""
        )
        result = client.delete("/work_packages/1")
        assert result == {}


class TestClientErrors:
    """Tests for client error handling."""

    @pytest.fixture
    def client(self, monkeypatch):
        """Create test client."""
        monkeypatch.delenv("OPENPROJECT_URL", raising=False)
        monkeypatch.delenv("OPENPROJECT_API_KEY", raising=False)
        c = OpenProjectClient(base_url="https://test.com", api_key="testkey")
        yield c
        c.close()

    def test_401_raises_auth_error(self, client, httpx_mock: HTTPXMock):
        """401 response raises AuthenticationError."""
        httpx_mock.add_response(
            url="https://test.com/api/v3/projects",
            status_code=401
        )
        with pytest.raises(AuthenticationError, match="Invalid API key"):
            client.get("/projects")

    def test_404_raises_api_error(self, client, httpx_mock: HTTPXMock):
        """404 response raises OpenProjectAPIError."""
        httpx_mock.add_response(
            url="https://test.com/api/v3/projects/999",
            status_code=404,
            json={
                "_type": "Error",
                "errorIdentifier": "urn:openproject-org:api:v3:errors:NotFound",
                "message": "The requested resource could not be found."
            }
        )
        with pytest.raises(OpenProjectAPIError) as exc_info:
            client.get("/projects/999")
        assert exc_info.value.status_code == 404
        assert "could not be found" in exc_info.value.message

    def test_500_raises_api_error(self, client, httpx_mock: HTTPXMock):
        """500 response raises OpenProjectAPIError."""
        httpx_mock.add_response(
            url="https://test.com/api/v3/projects",
            status_code=500,
            json={"message": "Internal Server Error"}
        )
        with pytest.raises(OpenProjectAPIError) as exc_info:
            client.get("/projects")
        assert exc_info.value.status_code == 500


class TestClientContextManager:
    """Tests for client context manager."""

    def test_context_manager(self, monkeypatch):
        """Client works as context manager."""
        monkeypatch.delenv("OPENPROJECT_URL", raising=False)
        monkeypatch.delenv("OPENPROJECT_API_KEY", raising=False)
        with OpenProjectClient(base_url="https://test.com", api_key="testkey") as client:
            assert client.base_url == "https://test.com"
        # Client should be closed after context
