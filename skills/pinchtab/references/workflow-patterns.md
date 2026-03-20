# PinchTab Workflow Patterns

Common automation patterns. All examples assume `BASE=http://localhost:9867` and active `$INST`, `$TAB` variables.

---

## 1. Web Scraping

Extract content from a website without interaction:

```bash
# Open page → extract text → close
TAB=$(curl -s -X POST "$BASE/instances/$INST/tabs/open" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://target-site.com/article"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# Get plain text (most token-efficient)
curl -s "$BASE/instances/$INST/tabs/$TAB/text"

# Close tab when done
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/close"
```

### Multi-page scraping

```bash
URLS=("https://site.com/page1" "https://site.com/page2" "https://site.com/page3")
for url in "${URLS[@]}"; do
  curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/navigate" \
    -H "Content-Type: application/json" -d "{\"url\":\"$url\"}"
  sleep 1
  curl -s "$BASE/instances/$INST/tabs/$TAB/text"
done
```

---

## 2. Form Submission

Login, signup, contact forms:

```bash
# 1. Navigate to form page
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/navigate" \
  -H "Content-Type: application/json" -d '{"url":"https://app.com/login"}'
sleep 1

# 2. Snapshot to discover form element refs
SNAPSHOT=$(curl -s "$BASE/instances/$INST/tabs/$TAB/snapshot")
echo "$SNAPSHOT" | python3 -m json.tool
# Look for input fields (e.g., e3=email, e5=password, e8=submit)

# 3. Fill fields
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/action" \
  -H "Content-Type: application/json" -d '{"type":"fill","ref":"e3","value":"user@example.com"}'
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/action" \
  -H "Content-Type: application/json" -d '{"type":"fill","ref":"e5","value":"mypassword"}'

# 4. Submit
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/action" \
  -H "Content-Type: application/json" -d '{"type":"click","ref":"e8"}'
sleep 2

# 5. Verify result
curl -s "$BASE/instances/$INST/tabs/$TAB/snapshot"
```

---

## 3. Multi-Tab Workflow

Work with multiple tabs simultaneously:

```bash
# Open tabs
TAB1=$(curl -s -X POST "$BASE/instances/$INST/tabs/open" \
  -H "Content-Type: application/json" -d '{"url":"https://source.com"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

TAB2=$(curl -s -X POST "$BASE/instances/$INST/tabs/open" \
  -H "Content-Type: application/json" -d '{"url":"https://destination.com"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# Read from tab1
DATA=$(curl -s "$BASE/instances/$INST/tabs/$TAB1/text")

# Use data in tab2 (e.g., paste into form)
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB2/action" \
  -H "Content-Type: application/json" -d "{\"type\":\"fill\",\"ref\":\"e3\",\"value\":\"$DATA\"}"
```

---

## 4. Search & Extract

Search on a website and extract results:

```bash
# Navigate to search page
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/navigate" \
  -H "Content-Type: application/json" -d '{"url":"https://site.com/search"}'
sleep 1

# Get snapshot to find search input
curl -s "$BASE/instances/$INST/tabs/$TAB/snapshot"

# Type search query and submit
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/action" \
  -H "Content-Type: application/json" -d '{"type":"fill","ref":"e2","value":"search query"}'
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/action" \
  -H "Content-Type: application/json" -d '{"type":"key","key":"Enter"}'
sleep 2

# Extract search results
curl -s "$BASE/instances/$INST/tabs/$TAB/text"
```

---

## 5. Profile Persistence (Session Reuse)

Reuse login sessions across automation runs:

```bash
# Create a named profile for the service
PROF=$(curl -s -X POST "$BASE/profiles" \
  -H "Content-Type: application/json" \
  -d '{"name":"gmail-session","description":"Gmail login session"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# First run: login manually or via automation
# Cookies persist in the profile directory

# Later runs: start instance with same profile — already logged in
INST=$(curl -s -X POST "$BASE/instances/start" \
  -H "Content-Type: application/json" \
  -d "{\"mode\":\"headless\",\"profile\":\"$PROF\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
```

---

## 6. Pagination

Navigate through paginated content:

```bash
PAGE=1
while true; do
  # Get current page content
  TEXT=$(curl -s "$BASE/instances/$INST/tabs/$TAB/text" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['text'])")
  echo "=== Page $PAGE ==="
  echo "$TEXT"

  # Find next button
  SNAP=$(curl -s "$BASE/instances/$INST/tabs/$TAB/snapshot")
  NEXT_REF=$(echo "$SNAP" | python3 -c "
import sys,json
tree = json.load(sys.stdin)['data']['tree']
for el in tree:
  if 'next' in el.get('text','').lower() and el.get('clickable'):
    print(el['ref']); break
else:
  print('NONE')
")

  [ "$NEXT_REF" = "NONE" ] && break

  curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/action" \
    -H "Content-Type: application/json" -d "{\"type\":\"click\",\"ref\":\"$NEXT_REF\"}"
  sleep 2
  PAGE=$((PAGE + 1))
done
```

---

## 7. Setup & Teardown Helper

Reusable pattern for any automation task:

```bash
BASE="http://localhost:9867"

# Setup
setup_pinchtab() {
  PROF=$(curl -s -X POST "$BASE/profiles" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$1\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
  INST=$(curl -s -X POST "$BASE/instances/start" \
    -H "Content-Type: application/json" \
    -d "{\"mode\":\"headless\",\"profile\":\"$PROF\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
  TAB=$(curl -s -X POST "$BASE/instances/$INST/tabs/open" \
    -H "Content-Type: application/json" \
    -d "{\"url\":\"$2\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
  echo "$PROF $INST $TAB"
}

# Teardown
teardown_pinchtab() {
  curl -s -X POST "$BASE/instances/$1/stop" > /dev/null
  curl -s -X DELETE "$BASE/profiles/$2" > /dev/null
}

# Usage
read PROF INST TAB <<< $(setup_pinchtab "task-name" "https://example.com")
# ... do work ...
teardown_pinchtab "$INST" "$PROF"
```

---

## Tips

- **Always snapshot before interacting** — element refs change when page content changes
- **Add `sleep 1-2`** after navigation/clicks that trigger page loads
- **Prefer `fill` over `type`** for form fields — `fill` clears existing content first
- **Use `text` endpoint** when you don't need to interact — saves tokens vs snapshot
- **Reuse profiles** for services requiring login — cookies persist across sessions
- **Check instance list** before creating new ones — `GET /instances` to avoid duplicates
