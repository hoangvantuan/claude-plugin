---
name: m365-onedrive
description: "Personal OneDrive files and folders via the m365 CLI: list, upload, download, move, share links, and restore versions."
allowed-tools:
  - Bash
  - Read
---

# m365-onedrive — Personal OneDrive Management

## Prerequisites

```bash
which m365 || echo "m365 CLI not installed. Run: npm i -g @pnp/cli-microsoft365"
m365 status || echo "Not signed in. Run: m365 login"
```

For auth details, see `../m365-shared/references/authentication.md`.

## Operating Principles

- OneDrive uses `spo file/folder` commands with OneDrive URL pattern: `https://{tenant}-my.sharepoint.com/personal/{user_encoded}`
- Always resolve OneDrive URL first before any file operation
- Output: always `-o json` with `--query`
- Default document library folder: `Documents`

---

## 1. Discover — Find OneDrive URL

### Auto-resolve Current User's OneDrive URL (non-admin)

Do NOT build the URL by hand: the SharePoint tenant name is often DIFFERENT from the email domain (e.g. `@miichisoft.com` → host `miichisoftjsc-my.sharepoint.com`), so string-joining with `sed` lands on the wrong host. Ask Microsoft Graph for the exact `webUrl` instead:

```bash
# webUrl of the personal OneDrive (non-admin). Graph returns ".../personal/<user>/Documents"
m365 request --url 'https://graph.microsoft.com/v1.0/me/drive?$select=webUrl' -o json --query 'webUrl'

# ONEDRIVE_URL for the spo commands = the site root (drop the trailing "/Documents"):
ONEDRIVE_URL=$(m365 request --url 'https://graph.microsoft.com/v1.0/me/drive?$select=webUrl' -o json --query 'webUrl' | tr -d '"' | sed 's#/Documents$##')
# e.g. https://miichisoftjsc-my.sharepoint.com/personal/tuanhv_miichisoft_com
```

### Check Storage Usage (non-admin)

```bash
m365 request --url 'https://graph.microsoft.com/v1.0/me/drive?$select=quota' -o json \
  --query 'quota.{usedBytes:used, totalBytes:total, remainingBytes:remaining}'
```

> `m365 onedrive list` is an **admin** command (403 for a regular user). The Graph `me/drive` route above works for every user.

---

## 2. File Operations

All file commands use `spo file` with the OneDrive web URL.

### List Files

```bash
# Root of Documents
m365 spo file list --webUrl "ONEDRIVE_URL" --folderUrl "Documents" -o json \
  --query '[].{name:Name, size:Length, modified:TimeLastModified, url:ServerRelativeUrl}'

# Specific subfolder
m365 spo file list --webUrl "ONEDRIVE_URL" --folderUrl "Documents/Projects" -o json \
  --query '[].{name:Name, size:Length}'

# Recursive (include subfolders)
m365 spo file list --webUrl "ONEDRIVE_URL" --folderUrl "Documents" --recursive -o json \
  --query '[].{name:Name, path:ServerRelativeUrl, size:Length}'

# Filter by name
m365 spo file list --webUrl "ONEDRIVE_URL" --folderUrl "Documents" \
  --filter "substringof('report',Name)" -o json --query '[].{name:Name}'
```

### Upload File

`spo file add` will soon default `--overwrite` to `false` — always set it explicitly to avoid the warning and surprises.

```bash
# Upload to root (overwrites a file with the same name)
m365 spo file add --webUrl "ONEDRIVE_URL" --folder "Documents" --path "/local/path/file.pdf" --overwrite true -o json

# Upload to subfolder
m365 spo file add --webUrl "ONEDRIVE_URL" --folder "Documents/Reports" --path "/local/path/report.xlsx" --overwrite true -o json

# Upload with custom name
m365 spo file add --webUrl "ONEDRIVE_URL" --folder "Documents" --path "/local/path/file.pdf" \
  --fileName "quarterly-report.pdf" --overwrite true -o json
```

### Download File

```bash
m365 spo file get --webUrl "ONEDRIVE_URL" --url "Documents/report.pdf" --asFile --path "/local/download/report.pdf"
```

### Copy File

```bash
m365 spo file copy --webUrl "ONEDRIVE_URL" \
  --sourceUrl "Documents/original.pdf" \
  --targetUrl "/personal/user_contoso_com/Documents/Archive" -o json

# Copy with new name
m365 spo file copy --webUrl "ONEDRIVE_URL" \
  --sourceUrl "Documents/original.pdf" \
  --targetUrl "/personal/user_contoso_com/Documents/Archive" \
  --newName "backup-original" -o json
```

### Move File

```bash
m365 spo file move --webUrl "ONEDRIVE_URL" \
  --sourceUrl "Documents/old-folder/file.pdf" \
  --targetUrl "/personal/user_contoso_com/Documents/new-folder" -o json
```

### Delete File

```bash
# Confirm with user first!
m365 spo file remove --webUrl "ONEDRIVE_URL" --url "Documents/unwanted.pdf" --force
```

---

## 3. Folder Operations

### List Folders

```bash
# Top-level folders
m365 spo folder list --webUrl "ONEDRIVE_URL" --parentFolderUrl "Documents" -o json \
  --query '[].{name:Name, url:ServerRelativeUrl, items:ItemCount}'

# Nested folders (recursive)
m365 spo folder list --webUrl "ONEDRIVE_URL" --parentFolderUrl "Documents" --recursive -o json \
  --query '[].{name:Name, path:ServerRelativeUrl}'
```

### Create Folder

```bash
m365 spo folder add --webUrl "ONEDRIVE_URL" --parentFolderUrl "Documents" --name "New Folder" -o json

# Create nested folder (auto-create parents)
m365 spo folder add --webUrl "ONEDRIVE_URL" --parentFolderUrl "Documents" \
  --name "Projects/2024/Q1" --ensureParentFolders true -o json
```

### Copy Folder

```bash
m365 spo folder copy --webUrl "ONEDRIVE_URL" \
  --sourceUrl "Documents/Project-A" \
  --targetUrl "/personal/user_contoso_com/Documents/Archive" -o json
```

### Move Folder

```bash
m365 spo folder move --webUrl "ONEDRIVE_URL" \
  --sourceUrl "Documents/Old-Folder" \
  --targetUrl "/personal/user_contoso_com/Documents/Archive" -o json
```

### Delete Folder

```bash
# Confirm with user first! (the correct option is --url, NOT --folderUrl)
m365 spo folder remove --webUrl "ONEDRIVE_URL" --url "Documents/Unwanted-Folder" --force
```

---

## 4. Sharing

### List Sharing Links

```bash
m365 spo file sharinglink list --webUrl "ONEDRIVE_URL" --fileUrl "Documents/shared-report.pdf" -o json \
  --query '[].{id:id, type:link.type, scope:link.scope, url:link.webUrl}'

# Filter by scope
m365 spo file sharinglink list --webUrl "ONEDRIVE_URL" --fileUrl "Documents/report.pdf" \
  --scope anonymous -o json
```

### Create Sharing Link

```bash
# View-only link (organization scope)
m365 spo file sharinglink add --webUrl "ONEDRIVE_URL" --fileUrl "Documents/report.pdf" \
  --type view --scope organization -o json

# Edit link (organization scope)
m365 spo file sharinglink add --webUrl "ONEDRIVE_URL" --fileUrl "Documents/report.pdf" \
  --type edit --scope organization -o json

# Anonymous link with expiration
m365 spo file sharinglink add --webUrl "ONEDRIVE_URL" --fileUrl "Documents/report.pdf" \
  --type view --scope anonymous --expirationDateTime "2025-12-31T23:59:59Z" -o json
```

### Remove Sharing Link

```bash
m365 spo file sharinglink remove --webUrl "ONEDRIVE_URL" --fileUrl "Documents/report.pdf" \
  --id "LINK_ID" --force
```

---

## 5. Versions

### List File Versions

```bash
m365 spo file version list --webUrl "ONEDRIVE_URL" --fileUrl "Documents/report.xlsx" -o json \
  --query '[].{id:ID, version:VersionLabel, size:Size, modified:Created, modifiedBy:CreatedBy}'
```

### Get Specific Version

```bash
m365 spo file version get --webUrl "ONEDRIVE_URL" --fileUrl "Documents/report.xlsx" \
  --label "1.0" -o json
```

### Restore Version

```bash
m365 spo file version restore --webUrl "ONEDRIVE_URL" --fileUrl "Documents/report.xlsx" \
  --label "1.0" --force
```

---

## Workflow: Resolve URL + Upload

Complete workflow for uploading a file to OneDrive:

```bash
# 1. Resolve the OneDrive site root URL (non-admin, through Graph)
ONEDRIVE_URL=$(m365 request --url 'https://graph.microsoft.com/v1.0/me/drive?$select=webUrl' -o json --query 'webUrl' | tr -d '"' | sed 's#/Documents$##')

# 2. Upload (set --overwrite explicitly)
m365 spo file add --webUrl "$ONEDRIVE_URL" --folder "Documents" --path "/local/file.pdf" --overwrite true -o json
```

---

## References

| File | When to read |
|------|-------------|
| `../m365-shared/SKILL.md` | Output format, JMESPath, error handling |
| `../m365-shared/references/authentication.md` | Auth methods in detail |
| `../m365-sharepoint/SKILL.md` | When you need file operations on a SharePoint site (not personal OneDrive) |
