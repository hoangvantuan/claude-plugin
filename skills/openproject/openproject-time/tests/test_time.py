"""Tests for OpenProject Time Entries operations."""

import pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from time_entries import (
    list_time_entries, get_time_entry, create_time_entry,
    update_time_entry, delete_time_entry, list_activities,
    get_activity, log_time, get_user_time_today, get_work_package_time
)


@pytest.fixture
def mock_client():
    """Create mock client."""
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    return client


class TestTimeEntries:
    """Tests for time entries functions."""

    def test_list_time_entries(self, mock_client):
        """List all time entries."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "hours": "PT2H"}]}
        }

        with patch("time_entries.get_client", return_value=mock_client):
            entries = list(list_time_entries())

        assert len(entries) == 1
        assert entries[0]["hours"] == "PT2H"

    def test_list_time_entries_with_filters(self, mock_client):
        """List time entries with filters."""
        mock_client.get.return_value = {"_embedded": {"elements": []}}

        with patch("time_entries.get_client", return_value=mock_client):
            filters = [{"user": {"operator": "=", "values": ["me"]}}]
            list(list_time_entries(filters=filters))

        call_args = mock_client.get.call_args
        assert "filters" in call_args[1]["params"]

    def test_list_time_entries_with_sort(self, mock_client):
        """List time entries with sorting."""
        mock_client.get.return_value = {"_embedded": {"elements": []}}

        with patch("time_entries.get_client", return_value=mock_client):
            list(list_time_entries(sort_by=[("spent_on", "desc")]))

        call_args = mock_client.get.call_args
        assert "sortBy" in call_args[1]["params"]

    def test_get_time_entry(self, mock_client):
        """Get time entry by ID."""
        mock_client.get.return_value = {"id": 1, "hours": "PT2H"}

        with patch("time_entries.get_client", return_value=mock_client):
            entry = get_time_entry(1)

        assert entry["id"] == 1
        mock_client.get.assert_called_with("/time_entries/1")

    def test_create_time_entry_minimal(self, mock_client):
        """Create time entry with minimal data."""
        mock_client.post.return_value = {"id": 1}

        with patch("time_entries.get_client", return_value=mock_client):
            create_time_entry(work_package_id=123, hours=2.0)

        call_data = mock_client.post.call_args[0][1]
        assert call_data["hours"] == "PT2.0H"
        assert call_data["_links"]["workPackage"]["href"] == "/work_packages/123"

    def test_create_time_entry_full(self, mock_client):
        """Create time entry with all options."""
        mock_client.post.return_value = {"id": 1}

        with patch("time_entries.get_client", return_value=mock_client):
            create_time_entry(
                work_package_id=123,
                hours=1.5,
                activity_id=1,
                comment="Worked on feature",
                spent_on="2026-01-09",
                user_id=5
            )

        call_data = mock_client.post.call_args[0][1]
        assert call_data["hours"] == "PT1.5H"
        assert call_data["comment"]["raw"] == "Worked on feature"
        assert call_data["spentOn"] == "2026-01-09"
        assert call_data["_links"]["activity"]["href"] == "/time_entries/activities/1"
        assert call_data["_links"]["user"]["href"] == "/users/5"

    def test_update_time_entry_hours(self, mock_client):
        """Update time entry hours."""
        mock_client.patch.return_value = {"id": 1}

        with patch("time_entries.get_client", return_value=mock_client):
            update_time_entry(1, hours=3.0)

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["hours"] == "PT3.0H"

    def test_update_time_entry_comment(self, mock_client):
        """Update time entry comment."""
        mock_client.patch.return_value = {"id": 1}

        with patch("time_entries.get_client", return_value=mock_client):
            update_time_entry(1, comment="Updated comment")

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["comment"]["raw"] == "Updated comment"

    def test_update_time_entry_activity(self, mock_client):
        """Update time entry activity."""
        mock_client.patch.return_value = {"id": 1}

        with patch("time_entries.get_client", return_value=mock_client):
            update_time_entry(1, activity_id=2)

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["_links"]["activity"]["href"] == "/time_entries/activities/2"

    def test_delete_time_entry(self, mock_client):
        """Delete time entry."""
        mock_client.delete.return_value = {}

        with patch("time_entries.get_client", return_value=mock_client):
            delete_time_entry(1)

        mock_client.delete.assert_called_with("/time_entries/1")

    def test_list_activities(self, mock_client):
        """List activity types."""
        mock_client.get.return_value = {
            "activity": {
                "_links": {
                    "allowedValues": [
                        {"href": "/activities/1", "title": "Development"},
                        {"href": "/activities/2", "title": "Design"}
                    ]
                }
            }
        }

        with patch("time_entries.get_client", return_value=mock_client):
            activities = list(list_activities())

        assert len(activities) == 2
        assert activities[0]["title"] == "Development"

    def test_get_activity(self, mock_client):
        """Get activity type."""
        mock_client.get.return_value = {"id": 1, "name": "Development"}

        with patch("time_entries.get_client", return_value=mock_client):
            activity = get_activity(1)

        assert activity["name"] == "Development"
        mock_client.get.assert_called_with("/time_entries/activities/1")

    def test_log_time_alias(self, mock_client):
        """Test log_time is alias for create_time_entry."""
        mock_client.post.return_value = {"id": 1}

        with patch("time_entries.get_client", return_value=mock_client):
            log_time(work_package_id=123, hours=2.0, comment="Test")

        call_data = mock_client.post.call_args[0][1]
        assert call_data["hours"] == "PT2.0H"
        assert call_data["comment"]["raw"] == "Test"

    def test_get_user_time_today(self, mock_client):
        """Get user's time entries for today."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1}, {"id": 2}]}
        }

        with patch("time_entries.get_client", return_value=mock_client):
            entries = get_user_time_today()

        assert len(entries) == 2
        call_args = mock_client.get.call_args
        assert "filters" in call_args[1]["params"]

    def test_get_work_package_time(self, mock_client):
        """Get time entries for work package."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "hours": "PT2H"}]}
        }

        with patch("time_entries.get_client", return_value=mock_client):
            entries = get_work_package_time(123)

        assert len(entries) == 1
        call_args = mock_client.get.call_args
        assert "filters" in call_args[1]["params"]
