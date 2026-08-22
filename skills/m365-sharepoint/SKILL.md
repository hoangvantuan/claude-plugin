---
name: m365-sharepoint
description: "SharePoint Online via the m365 CLI: a group/team's Shared Documents, site files and folders, lists, list items, permissions, and site creation."
allowed-tools:
  - Bash
  - Read
---

# m365-sharepoint — SharePoint Online Management

## Prerequisites

```bash
which m365 || echo "m365 CLI not installed. Run: npm i -g @pnp/cli-microsoft365"
m365 status || echo "Not signed in. Run: m365 login"
```

For auth details, see `../m365-shared/references/authentication.md`.

## Operating Principles

- All commands require `--webUrl` pointing to the SharePoint site URL
- Output: always `-o json` with `--query`
- List/library identification: prefer `--listTitle` for readability, `--listId` when title is ambiguous
- File/folder URLs: can be server-relative (`/sites/project/Shared Documents/file.pdf`) or site-relative (`Shared Documents/file.pdf`)
- Destructive operations (remove, delete): always confirm with user first

---

## 1. Sites

> The most common case is **reaching the documents of a group/team you belong to** (NO admin rights needed). Resolve the group site URL through Graph, then use it as `SITE_URL` for **4. Files** / **5. Folders**. Group documents live in the **"Shared Documents"** library (the Files tab in Teams).

### Resolve Team/Group Site URL (non-admin)

```bash
# 1. List the groups/teams you joined and take the group id
m365 teams team list --joined -o json --query '[].{id:id, name:displayName}'

# 2. Get the group SITE_URL (webUrl) from the group id — non-admin, used by every spo command below
m365 request --url 'https://graph.microsoft.com/v1.0/groups/<GROUP_ID>/sites/root?$select=webUrl' -o json --query 'webUrl'
# e.g. https://miichisoftjsc.sharepoint.com/sites/AICLUB
```

### List Sites (admin)

> `spo site list` requires **SharePoint Administrator** — a regular user gets *Unauthorized*. To work with group documents, resolve the site through the group as shown above.

```bash
# All sites
m365 spo site list -o json --query '[].{url:Url, title:Title, template:Template}'

# Team sites only
m365 spo site list --type TeamSite -o json --query '[].{url:Url, title:Title}'

# Communication sites only
m365 spo site list --type CommunicationSite -o json --query '[].{url:Url, title:Title}'

# Filter by URL
m365 spo site list --filter "Url -like 'project'" -o json --query '[].{url:Url, title:Title}'
```

### Get Site Details

```bash
m365 spo site get --url "https://contoso.sharepoint.com/sites/project" -o json
```

### Create Site

```bash
# Team site (default)
m365 spo site add --type TeamSite --title "New Project" --alias "new-project" \
  --description "Project collaboration site" -o json

# Communication site
m365 spo site add --type CommunicationSite --title "Company News" \
  --url "https://contoso.sharepoint.com/sites/company-news" -o json

# Team site with owners
m365 spo site add --type TeamSite --title "HR Team" --alias "hr-team" \
  --owners "admin@contoso.com" -o json

# Classic site (with wait)
m365 spo site add --type ClassicSite --title "Archive" \
  --url "https://contoso.sharepoint.com/sites/archive" \
  --timeZone 4 --wait -o json
```

---

## 2. Lists

### List All Lists

```bash
m365 spo list list --webUrl "SITE_URL" -o json \
  --query '[].{id:Id, title:Title, items:ItemCount, template:BaseTemplate}'

# Filter by template
m365 spo list list --webUrl "SITE_URL" --filter "BaseTemplate eq 100" -o json \
  --query '[].{id:Id, title:Title}'
```

### Get List Details

```bash
# By title
m365 spo list get --webUrl "SITE_URL" --title "Tasks" -o json

# By ID
m365 spo list get --webUrl "SITE_URL" --id "LIST_GUID" -o json

# With permissions
m365 spo list get --webUrl "SITE_URL" --title "Tasks" --withPermissions -o json
```

### Create List

```bash
# Generic list
m365 spo list add --webUrl "SITE_URL" --title "Project Tasks" --baseTemplate GenericList -o json

# Document library
m365 spo list add --webUrl "SITE_URL" --title "Project Docs" --baseTemplate DocumentLibrary -o json

# With versioning
m365 spo list add --webUrl "SITE_URL" --title "Contracts" --baseTemplate DocumentLibrary \
  --enableVersioning true --majorVersionLimit 50 -o json

# Events/Calendar
m365 spo list add --webUrl "SITE_URL" --title "Team Events" --baseTemplate Events -o json
```

Common `--baseTemplate` values: `GenericList`, `DocumentLibrary`, `Events`, `Tasks`, `Contacts`, `Announcements`, `Links`, `Survey`, `IssuesTracking`.

---

## 3. List Items

### List Items

```bash
# All items
m365 spo listitem list --webUrl "SITE_URL" --listTitle "Tasks" -o json \
  --query '[].{id:Id, title:Title, status:Status}'

# With specific fields
m365 spo listitem list --webUrl "SITE_URL" --listTitle "Tasks" \
  --fields "Title,Status,AssignedTo,DueDate" -o json

# Filter
m365 spo listitem list --webUrl "SITE_URL" --listTitle "Tasks" \
  --filter "Status eq 'In Progress'" -o json \
  --query '[].{id:Id, title:Title, assignee:AssignedTo}'

# Pagination
m365 spo listitem list --webUrl "SITE_URL" --listTitle "Tasks" \
  --pageSize 100 --pageNumber 0 -o json

# CAML query
m365 spo listitem list --webUrl "SITE_URL" --listTitle "Tasks" \
  --camlQuery "<View><Query><Where><Eq><FieldRef Name='Status'/><Value Type='Text'>Done</Value></Eq></Where></Query><RowLimit>10</RowLimit></View>" -o json
```

### Get Item

```bash
m365 spo listitem get --webUrl "SITE_URL" --listTitle "Tasks" --id 42 -o json
```

### Add Item

```bash
m365 spo listitem add --webUrl "SITE_URL" --listTitle "Tasks" \
  --Title "New task" --Status "Not Started" --DueDate "2025-03-01 09:00:00" -o json

# With content type
m365 spo listitem add --webUrl "SITE_URL" --listTitle "Tasks" \
  --contentType "Task" --Title "New task" -o json
```

NOTE: DateTime fields must use local timezone format `yyyy-MM-dd HH:mm:ss` (NOT ISO 8601/UTC).

### Update Item

```bash
m365 spo listitem set --webUrl "SITE_URL" --listTitle "Tasks" --id 42 \
  --Status "In Progress" --AssignedTo "[{'Key':'i:0#.f|membership|user@contoso.com'}]" -o json
```

### Delete Item

```bash
# Confirm with user first!
m365 spo listitem remove --webUrl "SITE_URL" --listTitle "Tasks" --id 42 --force
```

---

## 4. Files

### List Files

```bash
# In document library root
m365 spo file list --webUrl "SITE_URL" --folderUrl "Shared Documents" -o json \
  --query '[].{name:Name, size:Length, modified:TimeLastModified}'

# In subfolder
m365 spo file list --webUrl "SITE_URL" --folderUrl "Shared Documents/Reports" -o json \
  --query '[].{name:Name, size:Length}'

# Recursive
m365 spo file list --webUrl "SITE_URL" --folderUrl "Shared Documents" --recursive -o json \
  --query '[].{name:Name, path:ServerRelativeUrl, size:Length}'

# Filter
m365 spo file list --webUrl "SITE_URL" --folderUrl "Shared Documents" \
  --filter "substringof('.pdf',Name)" -o json --query '[].{name:Name}'
```

### Upload File

```bash
m365 spo file add --webUrl "SITE_URL" --folder "Shared Documents" \
  --path "/local/path/report.pdf" -o json

# To subfolder
m365 spo file add --webUrl "SITE_URL" --folder "Shared Documents/Reports/2024" \
  --path "/local/path/q4-report.pdf" -o json

# With custom name
m365 spo file add --webUrl "SITE_URL" --folder "Shared Documents" \
  --path "/local/path/file.pdf" --fileName "quarterly-report.pdf" -o json

# With checkout/checkin
m365 spo file add --webUrl "SITE_URL" --folder "Shared Documents" \
  --path "/local/path/contract.docx" --checkOut true --checkInComment "Initial upload" -o json
```

### Download File

```bash
m365 spo file get --webUrl "SITE_URL" --url "Shared Documents/report.pdf" \
  --asFile --path "/local/download/report.pdf"
```

### Copy File

```bash
m365 spo file copy --webUrl "SITE_URL" \
  --sourceUrl "Shared Documents/report.pdf" \
  --targetUrl "/sites/archive/Shared Documents" -o json

# With conflict handling
m365 spo file copy --webUrl "SITE_URL" \
  --sourceUrl "Shared Documents/report.pdf" \
  --targetUrl "/sites/other-site/Shared Documents" \
  --nameConflictBehavior rename -o json
```

### Move File

```bash
m365 spo file move --webUrl "SITE_URL" \
  --sourceUrl "Shared Documents/old-folder/report.pdf" \
  --targetUrl "/sites/project/Shared Documents/new-folder" -o json
```

### Delete File

```bash
# Confirm with user first!
m365 spo file remove --webUrl "SITE_URL" --url "Shared Documents/unwanted.pdf" --force
```

### Check In/Out

```bash
# Check out (the correct option is --url, NOT --fileUrl)
m365 spo file checkout --webUrl "SITE_URL" --url "Shared Documents/contract.docx"

# Check in
m365 spo file checkin --webUrl "SITE_URL" --url "Shared Documents/contract.docx" \
  --comment "Updated section 3"
```

---

## 5. Folders

### List Folders

```bash
m365 spo folder list --webUrl "SITE_URL" --parentFolderUrl "Shared Documents" -o json \
  --query '[].{name:Name, url:ServerRelativeUrl, items:ItemCount}'

# Recursive
m365 spo folder list --webUrl "SITE_URL" --parentFolderUrl "Shared Documents" --recursive -o json \
  --query '[].{name:Name, path:ServerRelativeUrl}'
```

### Create Folder

```bash
m365 spo folder add --webUrl "SITE_URL" --parentFolderUrl "Shared Documents" --name "New Folder" -o json

# Nested (auto-create parents)
m365 spo folder add --webUrl "SITE_URL" --parentFolderUrl "Shared Documents" \
  --name "Projects/2024/Q1" --ensureParentFolders true -o json
```

### Copy / Move Folder

```bash
# Copy
m365 spo folder copy --webUrl "SITE_URL" \
  --sourceUrl "Shared Documents/Project-A" \
  --targetUrl "/sites/archive/Shared Documents" -o json

# Move
m365 spo folder move --webUrl "SITE_URL" \
  --sourceUrl "Shared Documents/Old-Folder" \
  --targetUrl "/sites/project/Shared Documents/Archive" -o json
```

### Delete Folder

```bash
# Confirm with user first! (the correct option is --url, NOT --folderUrl)
m365 spo folder remove --webUrl "SITE_URL" --url "Shared Documents/Unwanted" --force
```

---

## 6. Permissions

### List Site Users

```bash
m365 spo user list --webUrl "SITE_URL" -o json \
  --query '[].{id:Id, name:Title, email:Email, login:LoginName}'
```

### List Site Groups

```bash
m365 spo group list --webUrl "SITE_URL" -o json \
  --query '[].{id:Id, name:Title, owner:OwnerTitle}'

# Only associated groups (Owners, Members, Visitors)
m365 spo group list --webUrl "SITE_URL" --associatedGroupsOnly -o json
```

### Get Group Members

```bash
m365 spo group member list --webUrl "SITE_URL" --groupId GROUP_ID -o json \
  --query '[].{id:Id, name:Title, email:Email}'

m365 spo group member list --webUrl "SITE_URL" --groupName "Project Members" -o json
```

### Add User to Group

```bash
m365 spo group member add --webUrl "SITE_URL" --groupName "Project Members" \
  --userNames "user@contoso.com"

# Add multiple users
m365 spo group member add --webUrl "SITE_URL" --groupName "Project Members" \
  --userNames "user1@contoso.com,user2@contoso.com"
```

### Remove User from Group

```bash
m365 spo group member remove --webUrl "SITE_URL" --groupId GROUP_ID \
  --userName "user@contoso.com" --force
```

### File/Folder Sharing Links

```bash
# List sharing links for a file
m365 spo file sharinglink list --webUrl "SITE_URL" --fileUrl "Shared Documents/report.pdf" -o json \
  --query '[].{id:id, type:link.type, scope:link.scope, url:link.webUrl}'

# Create sharing link
m365 spo file sharinglink add --webUrl "SITE_URL" --fileUrl "Shared Documents/report.pdf" \
  --type view --scope organization -o json

# Remove sharing link
m365 spo file sharinglink remove --webUrl "SITE_URL" --fileUrl "Shared Documents/report.pdf" \
  --id "LINK_ID" --force
```

---

## References

| File | When to read |
|------|-------------|
| `references/advanced-commands.md` | Page, Search, Content Type, Hub Site, Site Design, Tenant Admin |
| `../m365-shared/SKILL.md` | Output format, JMESPath, error handling |
| `../m365-shared/references/authentication.md` | Auth methods in detail |
