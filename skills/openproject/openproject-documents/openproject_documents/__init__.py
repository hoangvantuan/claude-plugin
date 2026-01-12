"""OpenProject Documents - Document and attachment management.

NOTE: Documents API is read-only. Create/delete via web UI only.
"""

from .attachments import (
    delete_attachment,
    download_attachment,
    get_attachment,
    list_attachments,
    upload_attachment,
)
from .documents import get_document, list_documents
from .wiki import get_wiki_page, list_wiki_attachments, update_wiki_page

__all__ = [
    "get_attachment",
    "list_attachments",
    "download_attachment",
    "upload_attachment",
    "delete_attachment",
    "list_documents",
    "get_document",
    "get_wiki_page",
    "list_wiki_attachments",
    "update_wiki_page",
]
