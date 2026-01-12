---
name: openproject-core
description: Core utilities for OpenProject API v3 integration. Provides HTTP client with API Key auth, HAL+JSON parsing, pagination helpers, filter builders. Required by all other openproject-* skills. Use when setting up OpenProject integration or troubleshooting API issues.
---

# OpenProject Core

Base utilities for OpenProject API v3 integration.

## Setup

```bash
cd .claude/skills/openproject
uv sync
```

Configure `.env`:
```bash
OPENPROJECT_URL=https://your-openproject-instance.com
OPENPROJECT_API_KEY=your-api-key
```

## Package: `openproject_core`

### client.py
- `OpenProjectClient`: Main HTTP client class
- Methods: `get()`, `post()`, `patch()`, `delete()`, `check_connection()`
- `check_connection()`: Standalone function to verify API connectivity
- Auto-handles auth, errors, HAL parsing

### helpers.py
- `build_filters()`: Build filter JSON string
- `build_sort()`: Build sortBy JSON string
- `paginate()`: Auto-paginate through results
- `extract_id_from_href()`: Extract resource ID from HAL href

### hal_types.py
- `HALLink`: Link type definition
- `HALResponse`: Base response type
- `CollectionResponse`: Paginated collection
- `ErrorResponse`: Error format

### exceptions.py
- `OpenProjectError`: Base exception
- `AuthenticationError`: Auth failed
- `OpenProjectAPIError`: API error response

## Usage

**Always run from skill directory with `uv run`:**

```bash
cd .claude/skills/openproject
uv run python -c "YOUR_CODE"
```

### Check Connection

```python
from openproject_core import check_connection
from dotenv import load_dotenv

load_dotenv()  # Required!

status = check_connection()
if status["ok"]:
    print(f"Connected as {status['user']} ({status['login']})")
    print(f"URL: {status['url']}")
    print(f"Admin: {status['admin']}")
else:
    print(f"Connection failed: {status['error']}")
```

### Basic API Usage

```python
from openproject_core import OpenProjectClient, build_filters, paginate
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = OpenProjectClient()

# Check connection via client method
status = client.check_connection()
print(f"Connected: {status['ok']}")

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
