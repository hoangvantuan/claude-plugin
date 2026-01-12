"""Tests for OpenProject Queries operations."""

import pytest
from unittest.mock import MagicMock, patch
from openproject_queries import (
    list_queries, get_query, create_query, update_query,
    delete_query, star_query, unstar_query, get_query_default,
    get_available_columns
)


@pytest.fixture
def mock_client():
    """Create mock client."""
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    return client


class TestQueries:
    """Tests for queries functions."""

    def test_list_queries(self, mock_client):
        """List all queries."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "name": "My Query"}]}
        }

        with patch("openproject_queries.queries.get_client", return_value=mock_client):
            queries = list(list_queries())

        assert len(queries) == 1
        assert queries[0]["name"] == "My Query"

    def test_list_queries_by_project(self, mock_client):
        """List queries for project."""
        mock_client.get.return_value = {"_embedded": {"elements": []}}

        with patch("openproject_queries.queries.get_client", return_value=mock_client):
            list(list_queries(project_id=5))

        call_args = mock_client.get.call_args
        assert "filters" in call_args[1]["params"]

    def test_get_query(self, mock_client):
        """Get query by ID."""
        mock_client.get.return_value = {"id": 1, "name": "Test Query"}

        with patch("openproject_queries.queries.get_client", return_value=mock_client):
            query = get_query(1)

        assert query["id"] == 1
        mock_client.get.assert_called_with("/queries/1")

    def test_create_query_minimal(self, mock_client):
        """Create query with name only."""
        mock_client.post.return_value = {"id": 1}

        with patch("openproject_queries.queries.get_client", return_value=mock_client):
            create_query(name="Test Query")

        call_data = mock_client.post.call_args[0][1]
        assert call_data["name"] == "Test Query"
        assert call_data["public"] is False

    def test_create_query_full(self, mock_client):
        """Create query with all options."""
        mock_client.post.return_value = {"id": 1}

        with patch("openproject_queries.queries.get_client", return_value=mock_client):
            create_query(
                name="My Tasks",
                project_id=5,
                filters=[{"status": {"operator": "o", "values": None}}],
                columns=["id", "subject"],
                sort_by=[("dueDate", "asc")],
                group_by="priority",
                public=True
            )

        call_data = mock_client.post.call_args[0][1]
        assert call_data["name"] == "My Tasks"
        assert call_data["public"] is True
        assert call_data["filters"] == [{"status": {"operator": "o", "values": None}}]
        assert call_data["columns"] == ["id", "subject"]
        assert call_data["sortBy"] == [["dueDate", "asc"]]
        assert call_data["groupBy"] == "priority"
        assert call_data["_links"]["project"]["href"] == "/projects/5"

    def test_update_query_name(self, mock_client):
        """Update query name."""
        mock_client.patch.return_value = {"id": 1}

        with patch("openproject_queries.queries.get_client", return_value=mock_client):
            update_query(1, name="Updated Name")

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["name"] == "Updated Name"

    def test_update_query_filters(self, mock_client):
        """Update query filters."""
        mock_client.patch.return_value = {"id": 1}

        with patch("openproject_queries.queries.get_client", return_value=mock_client):
            update_query(1, filters=[{"status": {"operator": "c", "values": None}}])

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["filters"] == [{"status": {"operator": "c", "values": None}}]

    def test_delete_query(self, mock_client):
        """Delete query."""
        mock_client.delete.return_value = {}

        with patch("openproject_queries.queries.get_client", return_value=mock_client):
            delete_query(1)

        mock_client.delete.assert_called_with("/queries/1")

    def test_star_query(self, mock_client):
        """Star query."""
        mock_client.patch.return_value = {}

        with patch("openproject_queries.queries.get_client", return_value=mock_client):
            star_query(1)

        mock_client.patch.assert_called_with("/queries/1/star", {})

    def test_unstar_query(self, mock_client):
        """Unstar query."""
        mock_client.patch.return_value = {}

        with patch("openproject_queries.queries.get_client", return_value=mock_client):
            unstar_query(1)

        mock_client.patch.assert_called_with("/queries/1/unstar", {})

    def test_get_query_default(self, mock_client):
        """Get default query."""
        mock_client.get.return_value = {"name": "Default"}

        with patch("openproject_queries.queries.get_client", return_value=mock_client):
            query = get_query_default()

        mock_client.get.assert_called_with("/queries/default")

    def test_get_available_columns(self, mock_client):
        """Get available columns."""
        mock_client.get.return_value = {
            "columns": {
                "_links": {
                    "allowedValues": [
                        {"id": "id", "name": "ID"},
                        {"id": "subject", "name": "Subject"}
                    ]
                }
            }
        }

        with patch("openproject_queries.queries.get_client", return_value=mock_client):
            columns = get_available_columns()

        assert len(columns) == 2
