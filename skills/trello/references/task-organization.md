# Task Organization — Labels & Checklists

Read this file when the user needs to: assign/create labels, manage checklists and check items on cards.

## Labels

Valid colors: `black`, `blue`, `green`, `lime`, `orange`, `pink`, `purple`, `red`, `sky`, `yellow`, `null` (no color)

```bash
# View board labels
curl -s "https://api.trello.com/1/boards/{boardId}/labels?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, color}'

# Create a new label
curl -s -X POST "https://api.trello.com/1/labels?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Bug" \
  -d "color=red" \
  -d "idBoard={boardId}"

# Assign label to card
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/idLabels?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "value={labelId}"

# Remove label from card
curl -s -X DELETE "https://api.trello.com/1/cards/{cardId}/idLabels/{labelId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Update label
curl -s -X PUT "https://api.trello.com/1/labels/{labelId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=New Name" \
  -d "color=blue"
```

## Checklists

```bash
# View card checklists
curl -s "https://api.trello.com/1/cards/{cardId}/checklists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, checkItems}'

# Create a new checklist on a card
curl -s -X POST "https://api.trello.com/1/checklists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idCard={cardId}" \
  -d "name=Checklist Name"

# Add item to checklist
curl -s -X POST "https://api.trello.com/1/checklists/{checklistId}/checkItems?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "name=Task item name" \
  -d "checked=false" \
  -d "pos=bottom"

# Mark item complete / incomplete
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}/checkItem/{checkItemId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "state=complete"    # or "incomplete"

# Delete checklist item
curl -s -X DELETE "https://api.trello.com/1/checklists/{checklistId}/checkItems/{checkItemId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"

# Delete entire checklist
curl -s -X DELETE "https://api.trello.com/1/checklists/{checklistId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN"
```
