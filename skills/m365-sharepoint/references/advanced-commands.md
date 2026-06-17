# Advanced SharePoint Commands

## Pages

```bash
# List pages
m365 spo page list --webUrl "SITE_URL" -o json --query '[].{name:Name, title:Title, url:Url}'

# Get page
m365 spo page get --webUrl "SITE_URL" --name "home.aspx" -o json

# Create page
m365 spo page add --webUrl "SITE_URL" --name "new-page.aspx" --title "New Page" -o json

# Update page
m365 spo page set --webUrl "SITE_URL" --name "page.aspx" --title "Updated Title"

# Remove page
m365 spo page remove --webUrl "SITE_URL" --name "old-page.aspx" --force
```

## Search

```bash
# Basic search
m365 spo search --queryText "quarterly report" -o json

# Scoped to a site
m365 spo search --queryText "quarterly report" --webUrl "SITE_URL" -o json

# With specific properties
m365 spo search --queryText "quarterly report" --selectProperties "Title,Path,Author" -o json
```

## Content Types

```bash
# List content types on a site
m365 spo contenttype list --webUrl "SITE_URL" -o json \
  --query '[].{id:StringId, name:Name, group:Group}'

# List content types on a list
m365 spo contenttype list --webUrl "SITE_URL" --listTitle "Tasks" -o json

# Add content type
m365 spo contenttype add --webUrl "SITE_URL" --name "Custom Task" --id "0x0108" \
  --group "Custom Content Types" -o json
```

## Fields (Columns)

```bash
# List fields on a site
m365 spo field list --webUrl "SITE_URL" -o json \
  --query '[].{id:Id, name:InternalName, title:Title, type:TypeAsString}'

# List fields on a list
m365 spo field list --webUrl "SITE_URL" --listTitle "Tasks" -o json

# Add field
m365 spo field add --webUrl "SITE_URL" --listTitle "Tasks" \
  --xml '<Field Type="Text" DisplayName="Priority" Required="FALSE" />' -o json
```

## Hub Sites

```bash
# List hub sites
m365 spo hubsite list -o json --query '[].{id:ID, title:Title, url:SiteUrl}'

# Get hub site
m365 spo hubsite get --id "HUB_ID" -o json

# Connect site to hub (option đúng là --parentId, KHÔNG phải --hubSiteId)
m365 spo hubsite connect --url "SITE_URL" --parentId "HUB_ID"

# Disconnect
m365 spo hubsite disconnect --url "SITE_URL" --force
```

## Site Designs

```bash
# List site designs
m365 spo sitedesign list -o json --query '[].{id:Id, title:Title}'

# Apply site design
m365 spo sitedesign apply --id "DESIGN_ID" --webUrl "SITE_URL"
```

## Tenant Administration

```bash
# Get tenant settings
m365 spo tenant settings list -o json

# List recycle bin items
m365 spo tenant recyclebinitem list -o json --query '[].{url:Url, deleted:DeletionTime, size:StorageMaximumLevel}'

# Restore from recycle bin
m365 spo tenant recyclebinitem restore --siteUrl "SITE_URL"
```

## Role Definitions

```bash
# List role definitions (permission levels)
m365 spo roledefinition list --webUrl "SITE_URL" -o json \
  --query '[].{id:Id, name:Name, description:Description}'
```
