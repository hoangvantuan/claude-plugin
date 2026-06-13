# Collaboration — Members, Comments, Attachments

Read this file when the user needs to: manage members (assign, invite, remove from board), comment on cards, or attach files/URLs.

## Members

```bash
# View my info
curl -s "https://api.trello.com/1/members/me?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=fullName,username,id" | jq

# View board members
curl -s "https://api.trello.com/1/boards/{boardId}/members?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {fullName, username, id}'

# Assign member to card
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/idMembers?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "value={memberId}"

# Unassign member from card
curl -s -X DELETE "https://api.trello.com/1/cards/{cardId}/idMembers/{memberId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# View cards assigned to a member
curl -s "https://api.trello.com/1/members/{memberId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id,idBoard,idList" | jq

# Invite member to board via email
curl -s -X PUT "https://api.trello.com/1/boards/{boardId}/members?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{"email": "user@example.com", "type": "normal"}'
# type: admin, normal, observer

# Add member to board (already in workspace)
curl -s -X PUT "https://api.trello.com/1/boards/{boardId}/members/{memberId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "type=normal"

# Remove member from board
curl -s -X DELETE "https://api.trello.com/1/boards/{boardId}/members/{memberId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```

## Comments

```bash
# View card comments (via actions)
curl -s "https://api.trello.com/1/cards/{cardId}/actions?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&filter=commentCard" | jq '.[] | {date, text: .data.text, by: .memberCreator.fullName}'

# Add comment
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/actions/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "text=Comment content"

# Edit comment (requires actionId from viewing comments step)
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}/actions/{actionId}/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "text=Updated content"

# Delete comment
curl -s -X DELETE "https://api.trello.com/1/cards/{cardId}/actions/{actionId}/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```

## Attachments

```bash
# View card attachments
curl -s "https://api.trello.com/1/cards/{cardId}/attachments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, url}'

# Attach URL to card
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/attachments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "url=https://example.com/doc.pdf" \
  -d "name=Reference document"

# Upload file attachment
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/attachments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -F "file=@/path/to/file.pdf" \
  -F "name=Attached file"

# Delete attachment
curl -s -X DELETE "https://api.trello.com/1/cards/{cardId}/attachments/{attachmentId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```
