"""Tests for OpenProject Users operations."""

import pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from users import (
    list_users, get_user, create_user, update_user, delete_user,
    lock_user, unlock_user
)
from groups import list_groups, get_group, create_group, update_group, add_member, remove_member
from memberships import list_memberships, create_membership, update_membership, delete_membership


@pytest.fixture
def mock_client():
    """Create mock client."""
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    return client


class TestUsers:
    """Tests for users functions."""

    def test_list_users(self, mock_client):
        """List all users."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "login": "admin"}]}
        }

        with patch("users.get_client", return_value=mock_client):
            users = list(list_users())

        assert len(users) == 1
        assert users[0]["login"] == "admin"

    def test_get_user(self, mock_client):
        """Get user by ID."""
        mock_client.get.return_value = {"id": 1, "login": "admin"}

        with patch("users.get_client", return_value=mock_client):
            user = get_user(1)

        assert user["id"] == 1
        mock_client.get.assert_called_with("/users/1")

    def test_get_current_user(self, mock_client):
        """Get current user via 'me'."""
        mock_client.get.return_value = {"id": 5, "login": "me"}

        with patch("users.get_client", return_value=mock_client):
            user = get_user("me")

        mock_client.get.assert_called_with("/users/me")

    def test_create_user_minimal(self, mock_client):
        """Create user with email only."""
        mock_client.post.return_value = {"id": 1, "email": "test@example.com"}

        with patch("users.get_client", return_value=mock_client):
            user = create_user(email="test@example.com")

        call_data = mock_client.post.call_args[0][1]
        assert call_data["email"] == "test@example.com"
        assert call_data["login"] == "test"  # derived from email
        assert call_data["status"] == "invited"

    def test_create_user_full(self, mock_client):
        """Create user with all fields."""
        mock_client.post.return_value = {"id": 1}

        with patch("users.get_client", return_value=mock_client):
            create_user(
                email="john@example.com",
                login="john",
                first_name="John",
                last_name="Doe",
                password="secret123",
                status="active",
                admin=True
            )

        call_data = mock_client.post.call_args[0][1]
        assert call_data["firstName"] == "John"
        assert call_data["lastName"] == "Doe"
        assert call_data["password"] == "secret123"
        assert call_data["admin"] is True

    def test_update_user(self, mock_client):
        """Update user fields."""
        mock_client.patch.return_value = {"id": 1}

        with patch("users.get_client", return_value=mock_client):
            update_user(1, first_name="Jane", admin=False)

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["firstName"] == "Jane"
        assert call_data["admin"] is False

    def test_delete_user(self, mock_client):
        """Delete user."""
        mock_client.delete.return_value = {}

        with patch("users.get_client", return_value=mock_client):
            delete_user(1)

        mock_client.delete.assert_called_with("/users/1")

    def test_lock_user(self, mock_client):
        """Lock user account."""
        mock_client.post.return_value = {}

        with patch("users.get_client", return_value=mock_client):
            lock_user(1)

        mock_client.post.assert_called_with("/users/1/lock")

    def test_unlock_user(self, mock_client):
        """Unlock user account."""
        mock_client.delete.return_value = {}

        with patch("users.get_client", return_value=mock_client):
            unlock_user(1)

        mock_client.delete.assert_called_with("/users/1/lock")


class TestGroups:
    """Tests for groups functions."""

    def test_list_groups(self, mock_client):
        """List all groups."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "name": "Developers"}]}
        }

        with patch("groups.get_client", return_value=mock_client):
            groups = list(list_groups())

        assert len(groups) == 1
        assert groups[0]["name"] == "Developers"

    def test_create_group(self, mock_client):
        """Create group."""
        mock_client.post.return_value = {"id": 1, "name": "New Group"}

        with patch("groups.get_client", return_value=mock_client):
            create_group("New Group")

        call_data = mock_client.post.call_args[0][1]
        assert call_data["name"] == "New Group"

    def test_create_group_with_members(self, mock_client):
        """Create group with initial members."""
        mock_client.post.return_value = {"id": 1}

        with patch("groups.get_client", return_value=mock_client):
            create_group("Team", member_ids=[1, 2, 3])

        call_data = mock_client.post.call_args[0][1]
        assert len(call_data["_links"]["members"]) == 3

    def test_update_group(self, mock_client):
        """Update group name."""
        mock_client.patch.return_value = {"id": 1}

        with patch("groups.get_client", return_value=mock_client):
            update_group(1, name="Updated Name")

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["name"] == "Updated Name"


class TestMemberships:
    """Tests for memberships functions."""

    def test_list_memberships(self, mock_client):
        """List all memberships."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1}]}
        }

        with patch("memberships.get_client", return_value=mock_client):
            memberships = list(list_memberships())

        assert len(memberships) == 1

    def test_list_memberships_by_project(self, mock_client):
        """List memberships for specific project."""
        mock_client.get.return_value = {"_embedded": {"elements": []}}

        with patch("memberships.get_client", return_value=mock_client):
            list(list_memberships(project_id=5))

        call_args = mock_client.get.call_args
        assert "filters" in call_args[1]["params"]

    def test_create_membership(self, mock_client):
        """Create membership."""
        mock_client.post.return_value = {"id": 1}

        with patch("memberships.get_client", return_value=mock_client):
            create_membership(project_id=5, principal_id=10, role_ids=[3, 4])

        call_data = mock_client.post.call_args[0][1]
        assert call_data["_links"]["project"]["href"] == "/projects/5"
        assert call_data["_links"]["principal"]["href"] == "/principals/10"
        assert len(call_data["_links"]["roles"]) == 2

    def test_update_membership(self, mock_client):
        """Update membership roles."""
        mock_client.patch.return_value = {"id": 1}

        with patch("memberships.get_client", return_value=mock_client):
            update_membership(1, role_ids=[5])

        call_data = mock_client.patch.call_args[0][1]
        assert len(call_data["_links"]["roles"]) == 1

    def test_delete_membership(self, mock_client):
        """Delete membership."""
        mock_client.delete.return_value = {}

        with patch("memberships.get_client", return_value=mock_client):
            delete_membership(1)

        mock_client.delete.assert_called_with("/memberships/1")
