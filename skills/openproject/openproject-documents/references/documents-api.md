# Documents API Reference

## Document Model

Key fields:
- `id`: Document ID
- `title`: Document title
- `description`: Document description
- `createdAt`, `updatedAt`: Timestamps

## Attachment Model

Key fields:
- `id`: Attachment ID
- `fileName`: Original filename
- `fileSize`: Size in bytes
- `contentType`: MIME type
- `digest`: File hash

## Links

- `self`: Resource URL
- `downloadLocation`: Direct download URL
- `uploadLink`: Upload URL (in prepare response)

## Upload Flow

1. **Prepare**: POST to `/containers/{id}/attachments/prepare`
2. **Upload**: PUT file to `uploadLink` URL

```python
# Step 1: Prepare
prepare_data = {
    "fileName": "report.pdf",
    "fileSize": 1024
}
prepared = client.post("/work_packages/123/attachments/prepare", prepare_data)

# Step 2: Upload
upload_url = prepared["_links"]["uploadLink"]["href"]
client.put(upload_url, content=file_bytes)
```

## Container Types

| Type | Endpoint |
|------|----------|
| work_packages | `/work_packages/{id}/attachments` |
| documents | `/documents/{id}/attachments` |
| wiki_pages | `/wiki_pages/{id}/attachments` |

## Wiki Page Model

Key fields:
- `id`: Page ID
- `title`: Page title
- `text`: Content (raw markdown)
- `_links.project`: Parent project
