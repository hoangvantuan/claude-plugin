"""Tests for OpenProject Notifications operations."""

import pytest
from unittest.mock import MagicMock, patch
from openproject_notifications import (
    list_notifications, get_notification, mark_read, mark_unread,
    mark_all_read, get_unread_count, list_unread, list_by_reason
)


@pytest.fixture
def mock_client():
    """Create mock client."""
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    return client


class TestNotifications:
    """Tests for notifications functions."""

    def test_list_notifications(self, mock_client):
        """List all notifications."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "reason": "mentioned"}]}
        }

        with patch("openproject_notifications.notifications.get_client", return_value=mock_client):
            notifications = list(list_notifications())

        assert len(notifications) == 1
        assert notifications[0]["reason"] == "mentioned"

    def test_list_notifications_unread(self, mock_client):
        """List unread notifications."""
        mock_client.get.return_value = {"_embedded": {"elements": []}}

        with patch("openproject_notifications.notifications.get_client", return_value=mock_client):
            list(list_notifications(read_status=False))

        call_args = mock_client.get.call_args
        assert "filters" in call_args[1]["params"]

    def test_list_notifications_by_reason(self, mock_client):
        """List notifications by reason."""
        mock_client.get.return_value = {"_embedded": {"elements": []}}

        with patch("openproject_notifications.notifications.get_client", return_value=mock_client):
            list(list_notifications(reason="assigned"))

        call_args = mock_client.get.call_args
        assert "filters" in call_args[1]["params"]

    def test_get_notification(self, mock_client):
        """Get notification by ID."""
        mock_client.get.return_value = {"id": 1, "reason": "mentioned"}

        with patch("openproject_notifications.notifications.get_client", return_value=mock_client):
            notification = get_notification(1)

        assert notification["id"] == 1
        mock_client.get.assert_called_with("/notifications/1")

    def test_mark_read(self, mock_client):
        """Mark notification as read."""
        mock_client.post.return_value = {}

        with patch("openproject_notifications.notifications.get_client", return_value=mock_client):
            mark_read(1)

        mock_client.post.assert_called_with("/notifications/1/read_ian", {})

    def test_mark_unread(self, mock_client):
        """Mark notification as unread."""
        mock_client.post.return_value = {}

        with patch("openproject_notifications.notifications.get_client", return_value=mock_client):
            mark_unread(1)

        mock_client.post.assert_called_with("/notifications/1/unread_ian", {})

    def test_mark_all_read(self, mock_client):
        """Mark all notifications as read."""
        mock_client.post.return_value = {}

        with patch("openproject_notifications.notifications.get_client", return_value=mock_client):
            mark_all_read()

        mock_client.post.assert_called_with("/notifications/read_ian", {})

    def test_get_unread_count(self, mock_client):
        """Get unread notification count."""
        mock_client.get.return_value = {"total": 5}

        with patch("openproject_notifications.notifications.get_client", return_value=mock_client):
            count = get_unread_count()

        assert count == 5

    def test_list_unread(self, mock_client):
        """List unread notifications."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1}]}
        }

        with patch("openproject_notifications.notifications.get_client", return_value=mock_client):
            notifications = list(list_unread())

        assert len(notifications) == 1

    def test_list_by_reason(self, mock_client):
        """List notifications by reason."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "reason": "assigned"}]}
        }

        with patch("openproject_notifications.notifications.get_client", return_value=mock_client):
            notifications = list(list_by_reason("assigned"))

        assert len(notifications) == 1
