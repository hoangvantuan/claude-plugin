"""Tests for OpenProject Admin operations."""

import pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from config import get_configuration
from wp_types import list_types, get_type, list_project_types
from statuses import list_statuses, get_status, list_open_statuses, list_closed_statuses
from roles import list_roles, get_role
from priorities import list_priorities, get_priority, get_default_priority


@pytest.fixture
def mock_client():
    """Create mock client."""
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    return client


class TestConfig:
    """Tests for configuration functions."""

    def test_get_configuration(self, mock_client):
        """Get system configuration."""
        mock_client.get.return_value = {"dateFormat": "YYYY-MM-DD"}

        with patch("config.get_client", return_value=mock_client):
            config = get_configuration()

        assert config["dateFormat"] == "YYYY-MM-DD"
        mock_client.get.assert_called_with("/configuration")


class TestTypes:
    """Tests for types functions."""

    def test_list_types(self, mock_client):
        """List work package types."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "name": "Task"}]}
        }

        with patch("wp_types.get_client", return_value=mock_client):
            types = list(list_types())

        assert len(types) == 1
        assert types[0]["name"] == "Task"

    def test_get_type(self, mock_client):
        """Get type by ID."""
        mock_client.get.return_value = {"id": 1, "name": "Task", "color": "#1A67A3"}

        with patch("wp_types.get_client", return_value=mock_client):
            wp_type = get_type(1)

        assert wp_type["name"] == "Task"
        mock_client.get.assert_called_with("/types/1")

    def test_list_project_types(self, mock_client):
        """List types for project."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1}]}
        }

        with patch("wp_types.get_client", return_value=mock_client):
            types = list(list_project_types(5))

        assert len(types) == 1


class TestStatuses:
    """Tests for statuses functions."""

    def test_list_statuses(self, mock_client):
        """List all statuses."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "name": "New", "isClosed": False}]}
        }

        with patch("statuses.get_client", return_value=mock_client):
            statuses = list(list_statuses())

        assert len(statuses) == 1
        assert statuses[0]["name"] == "New"

    def test_get_status(self, mock_client):
        """Get status by ID."""
        mock_client.get.return_value = {"id": 1, "name": "New", "isClosed": False}

        with patch("statuses.get_client", return_value=mock_client):
            status = get_status(1)

        assert status["name"] == "New"
        mock_client.get.assert_called_with("/statuses/1")

    def test_list_open_statuses(self, mock_client):
        """List open statuses only."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [
                {"id": 1, "name": "New", "isClosed": False},
                {"id": 2, "name": "Closed", "isClosed": True}
            ]}
        }

        with patch("statuses.get_client", return_value=mock_client):
            statuses = list(list_open_statuses())

        assert len(statuses) == 1
        assert statuses[0]["name"] == "New"

    def test_list_closed_statuses(self, mock_client):
        """List closed statuses only."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [
                {"id": 1, "name": "New", "isClosed": False},
                {"id": 2, "name": "Closed", "isClosed": True}
            ]}
        }

        with patch("statuses.get_client", return_value=mock_client):
            statuses = list(list_closed_statuses())

        assert len(statuses) == 1
        assert statuses[0]["name"] == "Closed"


class TestRoles:
    """Tests for roles functions."""

    def test_list_roles(self, mock_client):
        """List all roles."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "name": "Member"}]}
        }

        with patch("roles.get_client", return_value=mock_client):
            roles = list(list_roles())

        assert len(roles) == 1
        assert roles[0]["name"] == "Member"

    def test_get_role(self, mock_client):
        """Get role by ID."""
        mock_client.get.return_value = {"id": 1, "name": "Member", "permissions": ["view_work_packages"]}

        with patch("roles.get_client", return_value=mock_client):
            role = get_role(1)

        assert role["name"] == "Member"
        assert "view_work_packages" in role["permissions"]
        mock_client.get.assert_called_with("/roles/1")


class TestPriorities:
    """Tests for priorities functions."""

    def test_list_priorities(self, mock_client):
        """List all priorities."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 10, "name": "Normal"}]}
        }

        with patch("priorities.get_client", return_value=mock_client):
            priorities = list(list_priorities())

        assert len(priorities) == 1
        assert priorities[0]["name"] == "Normal"

    def test_get_priority(self, mock_client):
        """Get priority by ID."""
        mock_client.get.return_value = {"id": 10, "name": "Normal", "isDefault": True}

        with patch("priorities.get_client", return_value=mock_client):
            priority = get_priority(10)

        assert priority["name"] == "Normal"
        mock_client.get.assert_called_with("/priorities/10")

    def test_get_default_priority(self, mock_client):
        """Get default priority."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [
                {"id": 9, "name": "High", "isDefault": False},
                {"id": 10, "name": "Normal", "isDefault": True}
            ]}
        }

        with patch("priorities.get_client", return_value=mock_client):
            priority = get_default_priority()

        assert priority["name"] == "Normal"
        assert priority["isDefault"] is True
