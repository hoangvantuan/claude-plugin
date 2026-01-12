"""Tests for OpenProject Work Packages operations."""

import pytest
from unittest.mock import MagicMock, patch

from openproject_work_packages import (
    list_work_packages,
    get_work_package,
    create_work_package,
    update_work_package,
    delete_work_package,
    list_activities,
    add_comment,
    list_relations,
    create_relation,
    delete_relation,
)
from openproject_work_packages.relations import RELATION_TYPES


@pytest.fixture
def mock_client():
    """Create mock client."""
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    return client


class TestListWorkPackages:
    """Tests for list_work_packages function."""

    def test_list_all_work_packages(self, mock_client):
        """List all work packages."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "subject": "Task 1"}]}
        }

        with patch("openproject_work_packages.work_packages.get_client", return_value=mock_client):
            wps = list(list_work_packages())

        assert len(wps) == 1
        assert wps[0]["subject"] == "Task 1"

    def test_list_project_work_packages(self, mock_client):
        """List work packages for specific project."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1}]}
        }

        with patch("openproject_work_packages.work_packages.get_client", return_value=mock_client):
            list(list_work_packages(project_id=5))

        # Should use project-scoped endpoint
        call_args = mock_client.get.call_args
        assert "/projects/5/work_packages" in call_args[0][0]

    def test_list_with_filters(self, mock_client):
        """List work packages with filters."""
        mock_client.get.return_value = {"_embedded": {"elements": []}}

        with patch("openproject_work_packages.work_packages.get_client", return_value=mock_client):
            list(list_work_packages(filters=[{"status": {"operator": "o", "values": []}}]))

        call_args = mock_client.get.call_args
        assert "filters" in call_args[1]["params"]


class TestGetWorkPackage:
    """Tests for get_work_package function."""

    def test_get_work_package(self, mock_client):
        """Get single work package."""
        mock_client.get.return_value = {"id": 1, "subject": "Test"}

        with patch("openproject_work_packages.work_packages.get_client", return_value=mock_client):
            wp = get_work_package(1)

        assert wp["id"] == 1
        mock_client.get.assert_called_with("/work_packages/1")


class TestCreateWorkPackage:
    """Tests for create_work_package function."""

    def test_create_minimal(self, mock_client):
        """Create work package with minimal fields."""
        mock_client.post.return_value = {"id": 1, "subject": "New Task"}

        with patch("openproject_work_packages.work_packages.get_client", return_value=mock_client):
            wp = create_work_package(project_id=5, subject="New Task")

        assert wp["subject"] == "New Task"
        call_data = mock_client.post.call_args[0][1]
        assert call_data["subject"] == "New Task"
        assert call_data["_links"]["project"]["href"] == "/projects/5"

    def test_create_full(self, mock_client):
        """Create work package with all options."""
        mock_client.post.return_value = {"id": 1}

        with patch("openproject_work_packages.work_packages.get_client", return_value=mock_client):
            create_work_package(
                project_id=5,
                subject="Full Task",
                type_id=1,
                description="Description",
                assignee_id=10,
                status_id=2,
                start_date="2024-01-15",
                due_date="2024-01-20",
                estimated_hours=8.0
            )

        call_data = mock_client.post.call_args[0][1]
        assert call_data["_links"]["type"]["href"] == "/types/1"
        assert call_data["_links"]["assignee"]["href"] == "/users/10"
        assert call_data["description"] == {"raw": "Description"}
        assert call_data["startDate"] == "2024-01-15"
        assert call_data["estimatedTime"] == "PT8.0H"


class TestUpdateWorkPackage:
    """Tests for update_work_package function."""

    def test_update_subject(self, mock_client):
        """Update work package subject."""
        mock_client.patch.return_value = {"id": 1, "subject": "Updated"}

        with patch("openproject_work_packages.work_packages.get_client", return_value=mock_client):
            update_work_package(1, subject="Updated")

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["subject"] == "Updated"

    def test_update_status(self, mock_client):
        """Update work package status."""
        mock_client.patch.return_value = {"id": 1}

        with patch("openproject_work_packages.work_packages.get_client", return_value=mock_client):
            update_work_package(1, status_id=3)

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["_links"]["status"]["href"] == "/statuses/3"

    def test_unassign(self, mock_client):
        """Unassign work package."""
        mock_client.patch.return_value = {"id": 1}

        with patch("openproject_work_packages.work_packages.get_client", return_value=mock_client):
            update_work_package(1, assignee_id=None)

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["_links"]["assignee"]["href"] is None


class TestDeleteWorkPackage:
    """Tests for delete_work_package function."""

    def test_delete(self, mock_client):
        """Delete work package."""
        mock_client.delete.return_value = {}

        with patch("openproject_work_packages.work_packages.get_client", return_value=mock_client):
            result = delete_work_package(1)

        assert result == {}
        mock_client.delete.assert_called_with("/work_packages/1")


class TestActivities:
    """Tests for activities functions."""

    def test_list_activities(self, mock_client):
        """List work package activities."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "_type": "Activity::Comment"}]}
        }

        with patch("openproject_work_packages.activities.get_client", return_value=mock_client):
            activities = list(list_activities(1))

        assert len(activities) == 1

    def test_add_comment(self, mock_client):
        """Add comment to work package."""
        mock_client.post.return_value = {"id": 1}

        with patch("openproject_work_packages.activities.get_client", return_value=mock_client):
            add_comment(1, "Test comment")

        call_data = mock_client.post.call_args[0][1]
        assert call_data["comment"] == {"raw": "Test comment"}


class TestRelations:
    """Tests for relations functions."""

    def test_list_relations(self, mock_client):
        """List work package relations."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "type": "blocks"}]}
        }

        with patch("openproject_work_packages.relations.get_client", return_value=mock_client):
            relations = list(list_relations(1))

        assert len(relations) == 1

    def test_create_relation(self, mock_client):
        """Create relation between work packages."""
        mock_client.post.return_value = {"id": 1}

        with patch("openproject_work_packages.relations.get_client", return_value=mock_client):
            create_relation(1, 2, "blocks")

        call_data = mock_client.post.call_args[0][1]
        assert call_data["type"] == "blocks"
        assert call_data["_links"]["from"]["href"] == "/work_packages/1"
        assert call_data["_links"]["to"]["href"] == "/work_packages/2"

    def test_create_relation_with_delay(self, mock_client):
        """Create relation with delay."""
        mock_client.post.return_value = {"id": 1}

        with patch("openproject_work_packages.relations.get_client", return_value=mock_client):
            create_relation(1, 2, "precedes", delay=5)

        call_data = mock_client.post.call_args[0][1]
        assert call_data["delay"] == 5

    def test_invalid_relation_type(self, mock_client):
        """Invalid relation type raises error."""
        with patch("openproject_work_packages.relations.get_client", return_value=mock_client):
            with pytest.raises(ValueError, match="Invalid relation type"):
                create_relation(1, 2, "invalid_type")

    def test_delete_relation(self, mock_client):
        """Delete relation."""
        mock_client.delete.return_value = {}

        with patch("openproject_work_packages.relations.get_client", return_value=mock_client):
            delete_relation(1)

        mock_client.delete.assert_called_with("/relations/1")
