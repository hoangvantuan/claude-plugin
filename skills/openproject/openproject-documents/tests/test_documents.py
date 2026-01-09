"""Tests for OpenProject Documents operations."""

import pytest
from unittest.mock import MagicMock, patch, mock_open
import sys
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from documents import list_documents, get_document, create_document, delete_document
from attachments import (
    get_attachment, list_attachments, download_attachment,
    upload_attachment, delete_attachment
)
from wiki import get_wiki_page, list_wiki_attachments, update_wiki_page


@pytest.fixture
def mock_client():
    """Create mock client."""
    client = MagicMock()
    client.__enter__ = MagicMock(return_value=client)
    client.__exit__ = MagicMock(return_value=False)
    return client


class TestDocuments:
    """Tests for documents functions."""

    def test_list_documents(self, mock_client):
        """List project documents."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1, "title": "Doc 1"}]}
        }

        with patch("documents.get_client", return_value=mock_client):
            docs = list(list_documents(project_id=5))

        assert len(docs) == 1
        assert docs[0]["title"] == "Doc 1"

    def test_get_document(self, mock_client):
        """Get document by ID."""
        mock_client.get.return_value = {"id": 1, "title": "Test Doc"}

        with patch("documents.get_client", return_value=mock_client):
            doc = get_document(1)

        assert doc["id"] == 1
        mock_client.get.assert_called_with("/documents/1")

    def test_create_document(self, mock_client):
        """Create document."""
        mock_client.post.return_value = {"id": 1}

        with patch("documents.get_client", return_value=mock_client):
            create_document(project_id=5, title="New Doc", description="Description")

        call_data = mock_client.post.call_args[0][1]
        assert call_data["title"] == "New Doc"
        assert call_data["description"]["raw"] == "Description"
        assert call_data["_links"]["project"]["href"] == "/projects/5"

    def test_delete_document(self, mock_client):
        """Delete document."""
        mock_client.delete.return_value = {}

        with patch("documents.get_client", return_value=mock_client):
            delete_document(1)

        mock_client.delete.assert_called_with("/documents/1")


class TestAttachments:
    """Tests for attachments functions."""

    def test_get_attachment(self, mock_client):
        """Get attachment metadata."""
        mock_client.get.return_value = {"id": 1, "fileName": "test.pdf"}

        with patch("attachments.get_client", return_value=mock_client):
            att = get_attachment(1)

        assert att["fileName"] == "test.pdf"
        mock_client.get.assert_called_with("/attachments/1")

    def test_list_attachments(self, mock_client):
        """List container attachments."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1}]}
        }

        with patch("attachments.get_client", return_value=mock_client):
            atts = list(list_attachments("work_packages", 123))

        assert len(atts) == 1

    def test_delete_attachment(self, mock_client):
        """Delete attachment."""
        mock_client.delete.return_value = {}

        with patch("attachments.get_client", return_value=mock_client):
            delete_attachment(1)

        mock_client.delete.assert_called_with("/attachments/1")


class TestWiki:
    """Tests for wiki functions."""

    def test_get_wiki_page(self, mock_client):
        """Get wiki page."""
        mock_client.get.return_value = {"id": 1, "title": "Wiki Page"}

        with patch("wiki.get_client", return_value=mock_client):
            page = get_wiki_page(1)

        assert page["title"] == "Wiki Page"
        mock_client.get.assert_called_with("/wiki_pages/1")

    def test_list_wiki_attachments(self, mock_client):
        """List wiki page attachments."""
        mock_client.get.return_value = {
            "_embedded": {"elements": [{"id": 1}]}
        }

        with patch("wiki.get_client", return_value=mock_client):
            atts = list(list_wiki_attachments(1))

        assert len(atts) == 1

    def test_update_wiki_page(self, mock_client):
        """Update wiki page."""
        mock_client.patch.return_value = {"id": 1}

        with patch("wiki.get_client", return_value=mock_client):
            update_wiki_page(1, title="New Title", text="New content")

        call_data = mock_client.patch.call_args[0][1]
        assert call_data["title"] == "New Title"
        assert call_data["text"]["raw"] == "New content"
