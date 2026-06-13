# Workspaces (Organizations)

Read this file when the user needs to manage workspaces: create, update, delete, view boards/members in a workspace, or create a board in a specific workspace.

```bash
# View all my workspaces
curl -s "https://api.trello.com/1/members/me/organizations?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=displayName,name,id,url" | jq '.[] | {displayName, name, id}'

# View workspace details
curl -s "https://api.trello.com/1/organizations/{orgId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=displayName,name,id,desc,url,memberships" | jq

# View boards in a workspace
curl -s "https://api.trello.com/1/organizations/{orgId}/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&filter=open&fields=name,id,url,closed" | jq '.[] | {name, id}'

# View workspace members
curl -s "https://api.trello.com/1/organizations/{orgId}/members?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {fullName, username, id}'

# Create a new workspace
curl -s -X POST "https://api.trello.com/1/organizations?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "displayName=Workspace Name" \
  -d "name=short-name" \
  -d "desc=Workspace description"

# Update workspace
curl -s -X PUT "https://api.trello.com/1/organizations/{orgId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "displayName=New Name" \
  -d "desc=New description"

# Delete workspace (warn user — deletes all boards inside)
curl -s -X DELETE "https://api.trello.com/1/organizations/{orgId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Create a board in a specific workspace
curl -s -X POST "https://api.trello.com/1/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Board Name" \
  -d "idOrganization={orgId}" \
  -d "defaultLists=false"
```

When the user has multiple workspaces, always ask or list workspaces first to determine the correct context.

`name` is the short name (used in URL), `displayName` is the full display name.
