# Advanced Workflows

Read this file when the user needs to: view board overview (snapshot, checklists overview), bulk move cards, view activity log, read plugin data, or make batch requests.

## View all checklists in a board (progress overview)

```bash
curl -s "https://api.trello.com/1/boards/{boardId}/checklists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, idCard, checkItems: [.checkItems[] | {name, state}]}'
```

## Get full board snapshot (single call)

```bash
curl -s "https://api.trello.com/1/boards/{boardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&lists=open&cards=open&card_fields=name,idList,desc,due,labels,dueComplete&labels=all&members=all&fields=name,id" | jq
```

## Move all cards from one list to another

```bash
curl -s -X POST "https://api.trello.com/1/lists/{sourceListId}/moveAllCards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idBoard={boardId}" \
  -d "idList={targetListId}"
```

## Get board activity log (N most recent actions)

```bash
curl -s "https://api.trello.com/1/boards/{boardId}/actions?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&limit=50" | jq '.[] | {type, date, memberCreator: .memberCreator.fullName}'
```

## Get pluginData (Power-Up data stored on card/board)

```bash
# Plugin data on card (e.g., data from active Power-Ups)
curl -s "https://api.trello.com/1/cards/{cardId}/pluginData?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq

# Board plugin data
curl -s "https://api.trello.com/1/boards/{boardId}/pluginData?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq

# View active Power-Ups on board
curl -s "https://api.trello.com/1/boards/{boardId}/boardPlugins?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {id, name: .idPlugin}'
```

## Batch request (up to 10 calls in 1 request)

```bash
curl -s "https://api.trello.com/1/batch?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&urls=/members/me/boards,/members/me/cards" | jq
```
