# Advanced commands — calendar groups, calendar sharing, the admin routes

The material here comes up far less often than what SKILL.md covers. Read it when the need actually arises.

## 1. Calendar groups

A calendar group is how Outlook bundles several calendars together ("My Calendars", "Team Calendars"). The `My Calendars` group is the default and always exists.

The native commands offer `get`, `list`, `set`, `remove` but **no `add`**, so creating a new group has to go through Graph.

```bash
USER=$(m365 status -o json --query 'connectedAs' | tr -d '"')

# List groups
m365 outlook calendargroup list --userName "$USER" -o json --query '[].{id:id, name:name, classId:classId}'

# Get one group
m365 outlook calendargroup get --userName "$USER" --name "My Calendars" -o json

# Rename a group
m365 outlook calendargroup set --userName "$USER" --id "GROUP_ID" --name "New name"

# Delete a group (the calendars inside go with it, ask the user first)
m365 outlook calendargroup remove --userName "$USER" --name "Group name" --force

# Create a group (no native command, go through Graph)
m365 request --url 'https://graph.microsoft.com/v1.0/me/calendarGroups' --method post \
  --content-type "application/json" --body '{"name":"Project calendars"}' -o json --query '{id:id, name:name}'
```

To create a calendar straight into a group, `outlook calendar add` already takes `--calendarGroupName`:

```bash
m365 outlook calendar add --userName "$USER" --name "Project Alpha" --calendarGroupName "Project calendars" -o json --query 'id'
```

## 2. Sharing a calendar with someone

No native command; go through Graph `calendarPermissions`.

```bash
# See who it is shared with
m365 request --url 'https://graph.microsoft.com/v1.0/me/calendar/calendarPermissions' -o json \
  --query 'value[].{who:emailAddress.name, role:role, id:id}'

# Share with one person
SP="${TMPDIR:-/tmp}"
cat > "$SP/perm.json" <<'JSON'
{
  "emailAddress": { "name": "Person A", "address": "persona@contoso.com" },
  "role": "read",
  "allowedRoles": ["read"]
}
JSON
m365 request --url 'https://graph.microsoft.com/v1.0/me/calendar/calendarPermissions' --method post \
  --content-type "application/json" --body "@$SP/perm.json" -o json --query '{id:id, role:role}'

# Revoke access
m365 request --url 'https://graph.microsoft.com/v1.0/me/calendar/calendarPermissions/PERMISSION_ID' --method delete -o none
```

The `role` levels: `freeBusyRead` (free/busy only), `limitedRead` (subjects visible), `read`, `write`, `delegateWithoutPrivateEventAccess`, `delegateWithPrivateEventAccess`, `custom`.

Sharing a calendar changes who can see your data, so confirm the recipient address and the permission level with the user before running it.

## 3. The admin-level meeting room routes

If an Exchange admin has granted `Place.Read.All`, these two routes work and are more stable than `beta/me/findRooms`:

```bash
# Native commands
m365 outlook room list -o json --query '[].{name:displayName, email:emailAddress}'
m365 outlook room list --roomlistEmail "building2@contoso.com" -o json
m365 outlook roomlist list -o json --query '[].{name:displayName, email:emailAddress}'

# Graph v1.0
m365 request --url 'https://graph.microsoft.com/v1.0/places/microsoft.graph.room' -o json \
  --query 'value[].{name:displayName, email:emailAddress, capacity:capacity, floor:floorLabel}'
```

Without the permission all three return 403, in which case use `beta/me/findRooms` from `graph-recipes.md`. The advantage of the admin route: it also carries `capacity` and `floorLabel`, which `findRooms` does not return.

## 4. What is unavailable with the m365 CLI default app

| Need | Endpoint | Status |
|------|----------|--------|
| working hours, preferred time zone | `me/mailboxSettings` | 403, missing `MailboxSettings.Read` |
| automatic replies | `me/mailboxSettings/automaticRepliesSetting` | 403, same reason |
| room list through `/places` | `v1.0/places/...` | 403, missing `Place.Read.All` |

Unlocking those scopes requires signing in with your own Microsoft Entra app (`m365 login --appId ...`) instead of the default one. That changes authentication for **all four** m365 skills, so if you need it, do it in `../m365-shared/references/authentication.md`, not here.
