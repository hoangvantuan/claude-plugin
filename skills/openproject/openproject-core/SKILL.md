---
name: openproject-core
description: Core utilities for OpenProject API v3 integration. Provides HTTP client with API Key auth, HAL+JSON parsing, pagination helpers, filter builders. Required by all other openproject-* skills. Use when setting up OpenProject integration or troubleshooting API issues.
---

# OpenProject Core

Base utilities for OpenProject API v3 integration.

## Setup

1. Set environment variables:
   - `OPENPROJECT_URL`: Your OpenProject instance URL
   - `OPENPROJECT_API_KEY`: Your API key (found in My Account)

2. Install dependencies:
```bash
pip install -r openproject-core/requirements.txt
```

## Scripts

### client.py
- `OpenProjectClient`: Main HTTP client class
- Methods: `get()`, `post()`, `patch()`, `delete()`
- Auto-handles auth, errors, HAL parsing

### helpers.py
- `build_filters()`: Build filter JSON string
- `build_sort()`: Build sortBy JSON string
- `paginate()`: Auto-paginate through results
- `parse_hal_response()`: Parse HAL+JSON responses
- `extract_id_from_href()`: Extract resource ID from HAL href

### types.py
- `HALLink`: Link type definition
- `HALResponse`: Base response type
- `CollectionResponse`: Paginated collection
- `ErrorResponse`: Error format

### exceptions.py
- `OpenProjectError`: Base exception
- `AuthenticationError`: Auth failed
- `OpenProjectAPIError`: API error response

## Usage

```python
from openproject_core.client import OpenProjectClient
from openproject_core.helpers import build_filters, paginate

# Initialize client
client = OpenProjectClient()

# Get work packages with filters
filters = build_filters([{"status": {"operator": "o", "values": []}}])
work_packages = client.get("/work_packages", params={"filters": filters})

# Paginate through all projects
for project in paginate(client, "/projects"):
    print(project["name"])

client.close()
```

## References
- `references/api-basics.md` - API fundamentals
