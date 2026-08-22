---
name: m365-teams
description: "Microsoft Teams via the m365 CLI: teams, channels, messages, chats, and members."
allowed-tools:
  - Bash
  - Read
---

# m365-teams — Microsoft Teams Management

## Prerequisites

```bash
# Check m365 CLI installed
which m365 || echo "m365 CLI not installed. Run: npm i -g @pnp/cli-microsoft365"

# Check logged in
m365 status || echo "Not signed in. Run: m365 login"
```

For auth details, see `../m365-shared/references/authentication.md`.

## Operating Principles

- Output: always `-o json` with `--query` to filter fields
- IDs: most commands accept both `--id` and `--name` — prefer `--name` for readability, use `--id` when name is ambiguous
- Message content supports HTML: `--message "<b>Bold</b> text"`
- Destructive operations (remove): always confirm with user first

---

## 1. Team CRUD

### List Teams

```bash
# All teams the user is a member of
m365 teams team list --joined -o json --query '[].{id:id, name:displayName, description:description}'

# All teams associated (including shared channels)
m365 teams team list --associated -o json --query '[].{id:id, name:displayName}'

# Another user's teams (requires Teams Admin role)
m365 teams team list --joined --userName john@contoso.com -o json --query '[].{id:id, name:displayName}'
```

### Get Team Details

```bash
# By name
m365 teams team get --name "Project Alpha" -o json

# By ID
m365 teams team get --id "TEAM_ID" -o json
```

### Create Team

```bash
# Basic
m365 teams team add --name "New Team" --description "Description here" --ownerUserNames "owner@contoso.com" --wait -o json

# With members
m365 teams team add --name "New Team" --description "Desc" \
  --ownerUserNames "owner@contoso.com" \
  --memberUserNames "user1@contoso.com,user2@contoso.com" \
  --wait -o json

# With multiple owners
m365 teams team add --name "New Team" --description "Desc" \
  --ownerEmails "owner1@contoso.com,owner2@contoso.com" \
  --wait -o json
```

Without `--wait`, returns an async operation object. With `--wait`, waits for provisioning and returns the group resource.

---

## 2. Channels

### List Channels

```bash
# All channels in a team
m365 teams channel list --teamName "Project Alpha" -o json --query '[].{id:id, name:displayName, type:membershipType}'

# Filter by type
m365 teams channel list --teamName "Project Alpha" --type private -o json --query '[].{id:id, name:displayName}'
```

### Get Channel

```bash
# By name
m365 teams channel get --teamName "Project Alpha" --name "General" -o json

# Get the primary (General) channel
m365 teams channel get --teamName "Project Alpha" --primary -o json
```

### Create Channel

```bash
# Standard channel
m365 teams channel add --teamName "Project Alpha" --name "Design" --description "Design discussions" -o json

# Private channel (requires --owner)
m365 teams channel add --teamName "Project Alpha" --name "Leadership" --type private --owner "owner@contoso.com" -o json

# Shared channel (requires --owner)
m365 teams channel add --teamName "Project Alpha" --name "Cross-team" --type shared --owner "owner@contoso.com" -o json
```

### Remove Channel

```bash
m365 teams channel remove --teamId "TEAM_ID" --name "Old Channel" --force
```

---

## 3. Messages (Channel)

### List Messages

```bash
# All messages in a channel (requires teamId + channelId)
m365 teams message list --teamId "TEAM_ID" --channelId "CHANNEL_ID" -o json \
  --query '[].{id:id, from:from.user.displayName, body:body.content, created:createdDateTime}'

# Messages since a date
m365 teams message list --teamId "TEAM_ID" --channelId "CHANNEL_ID" \
  --since "2024-01-01T00:00:00Z" -o json \
  --query '[].{id:id, from:from.user.displayName, body:body.content}'
```

### Send Message

```bash
# Plain text
m365 teams message send --teamId "TEAM_ID" --channelId "CHANNEL_ID" --message "Hello team!"

# HTML content
m365 teams message send --teamId "TEAM_ID" --channelId "CHANNEL_ID" \
  --message "<h2>Update</h2><p>New release is ready</p>"
```

### Get Message

```bash
m365 teams message get --teamId "TEAM_ID" --channelId "CHANNEL_ID" --id "MESSAGE_ID" -o json
```

### Workflow: Send a message to a channel by name

```bash
# Step 1: Get team ID
TEAM_ID=$(m365 teams team get --name "Project Alpha" -o json --query 'id' | tr -d '"')

# Step 2: Get channel ID
CHANNEL_ID=$(m365 teams channel get --teamId "$TEAM_ID" --name "General" -o json --query 'id' | tr -d '"')

# Step 3: Send message
m365 teams message send --teamId "$TEAM_ID" --channelId "$CHANNEL_ID" --message "Hello!"
```

---

## 4. Chat (1:1 and Group)

### List Chats

```bash
# All chats
m365 teams chat list -o json --query '[].{id:id, topic:topic, type:chatType}'

# Filter by type
m365 teams chat list --type oneOnOne -o json --query '[].{id:id, topic:topic}'
m365 teams chat list --type group -o json --query '[].{id:id, topic:topic}'
```

### List Chat Messages

```bash
m365 teams chat message list --chatId "CHAT_ID" -o json \
  --query '[].{id:id, from:from.user.displayName, body:body.content, created:createdDateTime}'
```

### Send Chat Message

```bash
# By chat ID
m365 teams chat message send --chatId "CHAT_ID" --message "Hi!"

# By email (creates new chat if none exists)
m365 teams chat message send --userEmails "user@contoso.com" --message "Hi!"

# Group chat by emails
m365 teams chat message send --userEmails "user1@contoso.com,user2@contoso.com" --message "Hello group!"

# By chat name
m365 teams chat message send --chatName "Project Chat" --message "Update here"

# HTML content
m365 teams chat message send --chatId "CHAT_ID" --message "<b>Important</b> update" --contentType html
```

NOTE: Chat message send only works with delegated permissions (not application).
NOTE: A successful send usually prints NOTHING to stdout — rely on the exit code (0 = sent); do not expect JSON back.

---

## 5. Members

### List Team Members

```bash
m365 teams user list --teamId "TEAM_ID" -o json --query '[].{id:id, name:displayName, email:userPrincipalName, role:userType}'

# Filter by role
m365 teams user list --teamId "TEAM_ID" --role Owner -o json --query '[].{name:displayName, email:userPrincipalName}'
m365 teams user list --teamId "TEAM_ID" --role Member -o json
m365 teams user list --teamId "TEAM_ID" --role Guest -o json
```

### List Channel Members

```bash
m365 teams channel member list --teamName "Project Alpha" --channelName "General" -o json \
  --query '[].{id:id, name:displayName, email:email, role:roles}'

# Filter by role
m365 teams channel member list --teamName "Project Alpha" --channelName "Private Channel" --role owner -o json
```

### Add Channel Member

```bash
# Add as member
m365 teams channel member add --teamName "Project Alpha" --channelName "Private Channel" \
  --userIds "user@contoso.com"

# Add as owner
m365 teams channel member add --teamName "Project Alpha" --channelName "Private Channel" \
  --userIds "user@contoso.com" --owner

# Add multiple
m365 teams channel member add --teamName "Project Alpha" --channelName "Private Channel" \
  --userIds "user1@contoso.com,user2@contoso.com"
```

NOTE: You can only add team members to a private channel. Add them to the team first if needed.

---

## References

| File | When to read |
|------|-------------|
| `references/advanced-commands.md` | When you need Tab, Meeting, App, Settings |
| `../m365-shared/SKILL.md` | Output format, JMESPath, error handling |
| `../m365-shared/references/authentication.md` | Auth methods in detail |
