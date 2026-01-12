"""Tests for OpenProject Projects operations."""

import pytest
from unittest.mock import MagicMock, patch

from openproject_projects import (
    list_projects,
    get_project,
    create_project,
    update_project,
    delete_project,
    copy_project,
    get_versions,
    get_categories,
    get_types,
    toggle_favorite,
)


@pytest.fixture
def mock_client():
    """Create mock client."""
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    return client


class TestListProjects:
    """Tests for list_projects function."""

    def test_list_projects_no_filters(self, mock_client):
        """List projects without filters."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "name": "Project 1"}]}
        }

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            projects = list(list_projects())

        assert len(projects) == 1
        assert projects[0]["name"] == "Project 1"

    def test_list_projects_with_filters(self, mock_client):
        """List projects with filters."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "name": "Active"}]}
        }

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            filters = [{"active": {"operator": "=", "values": ["t"]}}]
            projects = list(list_projects(filters=filters))

        assert len(projects) == 1
        # Verify filters were passed
        call_args = mock_client.get.call_args
        assert "filters" in call_args[1]["params"]

    def test_list_projects_with_sort(self, mock_client):
        """List projects with sorting."""
        mock_client.get.return_value = {
            "_embedded": {"elements": []}
        }

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            list(list_projects(sort_by=[("name", "asc")]))

        call_args = mock_client.get.call_args
        assert "sortBy" in call_args[1]["params"]


class TestGetProject:
    """Tests for get_project function."""

    def test_get_project_by_id(self, mock_client):
        """Get project by numeric ID."""
        mock_client.get.return_value = {"id": 1, "name": "Test Project"}

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            project = get_project(1)

        assert project["id"] == 1
        mock_client.get.assert_called_with("/projects/1")

    def test_get_project_by_identifier(self, mock_client):
        """Get project by string identifier."""
        mock_client.get.return_value = {"id": 1, "identifier": "test-project"}

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            project = get_project("test-project")

        assert project["identifier"] == "test-project"
        mock_client.get.assert_called_with("/projects/test-project")


class TestCreateProject:
    """Tests for create_project function."""

    def test_create_project_minimal(self, mock_client):
        """Create project with minimal fields."""
        mock_client.post.return_value = {"id": 1, "name": "New Project"}

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            project = create_project(name="New Project")

        assert project["name"] == "New Project"
        call_data = mock_client.post.call_args[0][1]
        assert call_data["name"] == "New Project"
        assert call_data["public"] is False

    def test_create_project_full(self, mock_client):
        """Create project with all fields."""
        mock_client.post.return_value = {"id": 1, "name": "Full Project"}

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            project = create_project(
                name="Full Project",
                identifier="full-project",
                description="A full project",
                public=True,
                parent_id=5
            )

        call_data = mock_client.post.call_args[0][1]
        assert call_data["name"] == "Full Project"
        assert call_data["identifier"] == "full-project"
        assert call_data["description"] == {"raw": "A full project"}
        assert call_data["public"] is True
        assert call_data["_links"]["parent"]["href"] == "/projects/5"


class TestUpdateProject:
    """Tests for update_project function."""

    def test_update_project_name(self, mock_client):
        """Update project name."""
        mock_client.patch.return_value = {"id": 1, "name": "Updated Name"}

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            project = update_project(1, name="Updated Name")

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["name"] == "Updated Name"

    def test_update_project_parent(self, mock_client):
        """Update project parent."""
        mock_client.patch.return_value = {"id": 1}

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            update_project(1, parent_id=5)

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["_links"]["parent"]["href"] == "/projects/5"

    def test_update_project_remove_parent(self, mock_client):
        """Remove project parent."""
        mock_client.patch.return_value = {"id": 1}

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            update_project(1, parent_id=None)

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["_links"]["parent"]["href"] is None


class TestDeleteProject:
    """Tests for delete_project function."""

    def test_delete_project(self, mock_client):
        """Delete project by ID."""
        mock_client.delete.return_value = {}

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            result = delete_project(1)

        assert result == {}
        mock_client.delete.assert_called_with("/projects/1")


class TestCopyProject:
    """Tests for copy_project function."""

    def test_copy_project_minimal(self, mock_client):
        """Copy project with new name only."""
        mock_client.post.return_value = {"id": 2, "name": "Copied Project"}

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            project = copy_project(1, "Copied Project")

        mock_client.post.assert_called_with(
            "/projects/1/copy",
            {"name": "Copied Project"}
        )

    def test_copy_project_with_identifier(self, mock_client):
        """Copy project with new identifier."""
        mock_client.post.return_value = {"id": 2}

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            copy_project(1, "Copied", new_identifier="copied-project")

        call_data = mock_client.post.call_args[0][1]
        assert call_data["identifier"] == "copied-project"


class TestGetVersions:
    """Tests for get_versions function."""

    def test_get_versions(self, mock_client):
        """Get project versions."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "name": "v1.0"}]}
        }

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            versions = list(get_versions(1))

        assert len(versions) == 1
        assert versions[0]["name"] == "v1.0"


class TestGetCategories:
    """Tests for get_categories function."""

    def test_get_categories(self, mock_client):
        """Get project categories."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "name": "Bug"}]}
        }

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            categories = list(get_categories(1))

        assert len(categories) == 1
        assert categories[0]["name"] == "Bug"


class TestGetTypes:
    """Tests for get_types function."""

    def test_get_types(self, mock_client):
        """Get project types."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "name": "Task"}]}
        }

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            types = list(get_types(1))

        assert len(types) == 1
        assert types[0]["name"] == "Task"


class TestToggleFavorite:
    """Tests for toggle_favorite function."""

    def test_add_favorite(self, mock_client):
        """Add project to favorites."""
        mock_client.post.return_value = {}

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            toggle_favorite(1, favorite=True)

        mock_client.post.assert_called_with("/projects/1/favorite")

    def test_remove_favorite(self, mock_client):
        """Remove project from favorites."""
        mock_client.delete.return_value = {}

        with patch("openproject_projects.projects.get_client", return_value=mock_client):
            toggle_favorite(1, favorite=False)

        mock_client.delete.assert_called_with("/projects/1/favorite")
