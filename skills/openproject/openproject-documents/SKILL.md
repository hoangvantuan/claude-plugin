---
name: openproject-documents
description: Manage OpenProject attachments and wiki pages via API v3. Upload/download attachments to work packages, wiki pages, posts, meetings. Documents API is read-only. Use when handling files, documentation, or wiki content.
---

# OpenProject Documents

Manage attachments, wiki pages, and documents.

## Prerequisites
- Environment: `OPENPROJECT_URL`, `OPENPROJECT_API_KEY` in `.env`
- Appropriate permissions for each operation

## Package: `openproject_documents`

### Attachments
- `get_attachment(id)` - Get attachment metadata
- `list_attachments(container_type, container_id)` - List attachments
- `download_attachment(id, path)` - Download file
- `upload_attachment(container_type, container_id, file_path)` - Upload file
- `delete_attachment(id)` - Delete attachment

**Valid container types:**
- `work_packages` ✓
- `wiki_pages` ✓
- `posts` ✓ (forum posts)
- `meetings` ✓
- `activities` ✓ (read-only)
- ~~`documents`~~ **NOT supported!**

### Documents (Read-Only)
- `list_documents()` - List all accessible documents
- `get_document(id)` - Get document details

**NOTE:** Documents API is **read-only**. Create/delete documents via OpenProject web UI only.

### Wiki
- `get_wiki_page(project_id, slug)` - Get wiki page
- `update_wiki_page(project_id, slug, content)` - Update wiki page

## Usage

**Always run from skill directory with `uv run`:**

```bash
cd .claude/skills/openproject
uv run python -c "YOUR_CODE"
```

### Examples

```python
from openproject_documents import (
    upload_attachment, download_attachment, list_attachments,
    list_documents, get_wiki_page
)
from dotenv import load_dotenv

load_dotenv()

# Upload file to work package
attachment = upload_attachment(
    container_type="work_packages",
    container_id=123,
    file_path="/path/to/file.pdf"
)
print(f"Uploaded: {attachment['fileName']}")

# List work package attachments
for att in list_attachments("work_packages", 123):
    print(f"{att['id']}: {att['fileName']}")

# Download attachment
download_attachment(456, "/path/to/output.pdf")

# List all documents (read-only, no project filter)
for doc in list_documents():
    print(f"{doc['id']}: {doc['title']}")

# Get wiki page
page = get_wiki_page(project_id=5, slug="home")
print(page["text"]["raw"])
```

## References
- `references/documents-api.md` - Full API details
