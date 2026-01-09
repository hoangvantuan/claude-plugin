---
name: openproject-documents
description: Manage OpenProject documents, attachments, and wiki pages via API v3. Upload/download attachments to work packages. Create/update wiki pages. Manage project documents. Use when handling files, documentation, or wiki content.
---

# OpenProject Documents

Manage documents, attachments, and wiki pages.

## Prerequisites
- `openproject-core` skill loaded
- Appropriate permissions for each operation

## Scripts

### scripts/documents.py
- `list_documents(project_id)` - List project documents
- `get_document(id)` - Get document
- `create_document(project_id, title, **kwargs)` - Create document

### scripts/attachments.py
- `get_attachment(id)` - Get attachment metadata
- `download_attachment(id, path)` - Download file
- `upload_attachment(container, id, file)` - Upload file
- `delete_attachment(id)` - Delete attachment

### scripts/wiki.py
- `get_wiki_page(id)` - Get wiki page
- `list_wiki_attachments(page_id)` - Get page attachments

## Quick Examples

```python
from attachments import upload_attachment, download_attachment

# Upload file to work package
upload_attachment("work_packages", 123, "/path/to/file.pdf")

# Download attachment
download_attachment(456, "/path/to/output.pdf")
```

## References
- `references/documents-api.md` - Full API details
