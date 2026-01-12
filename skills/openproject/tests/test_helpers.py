"""Tests for OpenProject helpers."""

import json
import pytest

from openproject_core import (
    build_filters,
    build_sort,
    parse_hal_response,
    extract_id_from_href,
    paginate,
)


class TestBuildFilters:
    """Tests for build_filters function."""

    def test_empty_filters(self):
        """Empty filter list returns empty JSON array."""
        result = build_filters([])
        assert result == "[]"

    def test_single_filter(self):
        """Single filter is properly serialized."""
        filters = [{"status": {"operator": "=", "values": ["1"]}}]
        result = build_filters(filters)
        parsed = json.loads(result)
        assert parsed == filters

    def test_multiple_filters(self):
        """Multiple filters are properly serialized."""
        filters = [
            {"status": {"operator": "o", "values": []}},
            {"project": {"operator": "=", "values": ["1", "2"]}}
        ]
        result = build_filters(filters)
        parsed = json.loads(result)
        assert len(parsed) == 2
        assert parsed[0]["status"]["operator"] == "o"
        assert parsed[1]["project"]["values"] == ["1", "2"]


class TestBuildSort:
    """Tests for build_sort function."""

    def test_empty_sort(self):
        """Empty sort list returns empty JSON array."""
        result = build_sort([])
        assert result == "[]"

    def test_single_sort(self):
        """Single sort field is properly serialized."""
        sort_by = [("updated_at", "desc")]
        result = build_sort(sort_by)
        parsed = json.loads(result)
        assert parsed == [["updated_at", "desc"]]

    def test_multiple_sort(self):
        """Multiple sort fields are properly serialized."""
        sort_by = [("updated_at", "desc"), ("id", "asc")]
        result = build_sort(sort_by)
        parsed = json.loads(result)
        assert parsed == [["updated_at", "desc"], ["id", "asc"]]


class TestParseHalResponse:
    """Tests for parse_hal_response function."""

    def test_minimal_response(self):
        """Minimal response parses correctly."""
        response = {"_type": "WorkPackage"}
        result = parse_hal_response(response)
        assert result["type"] == "WorkPackage"
        assert result["data"] == {}
        assert result["links"] == {}
        assert result["embedded"] == {}

    def test_full_response(self):
        """Full HAL response parses correctly."""
        response = {
            "_type": "WorkPackage",
            "id": 123,
            "subject": "Test",
            "_links": {
                "self": {"href": "/api/v3/work_packages/123"}
            },
            "_embedded": {
                "status": {"_type": "Status", "name": "New"}
            }
        }
        result = parse_hal_response(response)
        assert result["type"] == "WorkPackage"
        assert result["data"]["id"] == 123
        assert result["data"]["subject"] == "Test"
        assert "_type" not in result["data"]
        assert "_links" not in result["data"]
        assert result["links"]["self"]["href"] == "/api/v3/work_packages/123"
        assert result["embedded"]["status"]["name"] == "New"

    def test_empty_response(self):
        """Empty response parses without error."""
        response = {}
        result = parse_hal_response(response)
        assert result["type"] is None
        assert result["data"] == {}
        assert result["links"] == {}
        assert result["embedded"] == {}


class TestExtractIdFromHref:
    """Tests for extract_id_from_href function."""

    def test_valid_href(self):
        """Valid href returns integer ID."""
        assert extract_id_from_href("/api/v3/projects/5") == 5
        assert extract_id_from_href("/api/v3/work_packages/123") == 123

    def test_href_with_trailing_slash(self):
        """Href with trailing slash still works."""
        assert extract_id_from_href("/api/v3/projects/5/") == 5

    def test_empty_href(self):
        """Empty href returns None."""
        assert extract_id_from_href("") is None
        assert extract_id_from_href(None) is None

    def test_invalid_href(self):
        """Non-numeric ID returns None."""
        assert extract_id_from_href("/api/v3/projects/abc") is None
        assert extract_id_from_href("/api/v3/") is None


class TestPaginate:
    """Tests for paginate function."""

    def test_single_page(self):
        """Single page returns all items."""
        class MockClient:
            def get(self, path, params=None):
                return {
                    "_embedded": {"elements": [{"id": 1}, {"id": 2}]},
                    "total": 2
                }

        items = list(paginate(MockClient(), "/projects", page_size=10))
        assert len(items) == 2
        assert items[0]["id"] == 1

    def test_multiple_pages(self):
        """Multiple pages yields all items."""
        class MockClient:
            def __init__(self):
                self.call_count = 0

            def get(self, path, params=None):
                self.call_count += 1
                if self.call_count == 1:
                    return {"_embedded": {"elements": [{"id": 1}, {"id": 2}]}}
                else:
                    return {"_embedded": {"elements": [{"id": 3}]}}

        items = list(paginate(MockClient(), "/projects", page_size=2))
        assert len(items) == 3
        assert items[2]["id"] == 3

    def test_empty_collection(self):
        """Empty collection yields nothing."""
        class MockClient:
            def get(self, path, params=None):
                return {"_embedded": {"elements": []}}

        items = list(paginate(MockClient(), "/projects"))
        assert items == []

    def test_params_passed_through(self):
        """Custom params are passed to client."""
        class MockClient:
            def __init__(self):
                self.last_params = None

            def get(self, path, params=None):
                self.last_params = params
                return {"_embedded": {"elements": []}}

        client = MockClient()
        list(paginate(client, "/projects", params={"filters": "test"}))
        assert client.last_params["filters"] == "test"
        assert client.last_params["pageSize"] == 100
