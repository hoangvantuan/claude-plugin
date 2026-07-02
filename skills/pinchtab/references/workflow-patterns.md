# PinchTab Workflow Patterns

Common automation patterns using CLI (recommended) and HTTP API.

For HTTP examples, assume `BASE=http://localhost:9867` and active `$INST`, `$TAB` variables.

---

## 1. Web Scraping (Text Extraction)

Extract content without interaction — most token-efficient approach.

### CLI

```bash
pinchtab nav https://target-site.com/article
pinchtab text
```

### Multi-Page Scraping (CLI)

```bash
URLS=("https://site.com/page1" "https://site.com/page2" "https://site.com/page3")
for url in "${URLS[@]}"; do
  pinchtab nav "$url"
  sleep 1
  pinchtab text
done
```

### HTTP

```bash
TAB=$(curl -s -X POST "$BASE/instances/$INST/tabs/open" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://target-site.com/article"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

curl -s "$BASE/instances/$INST/tabs/$TAB/text"
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/close"
```

---

## 2. Form Submission (Login, Signup, Contact)

### CLI

```bash
pinchtab nav https://app.com/login
pinchtab snap -i                            # interactive elements only
# → e3=email, e5=password, e8=submit

pinchtab fill e3 "user@example.com"
pinchtab fill e5 "mypassword"
pinchtab click e8
sleep 2
pinchtab snap                               # verify result
```

### HTTP

```bash
curl -s -X POST "$BASE/instances/$INST/tabs/$TAB/navigate" \
  -H "Content-Type: application/json" -d '{"url":"https://app.com/login"}'
sleep 1

curl -s "$BASE/instances/$INST/tabs/$TAB/snapshot"

# Batch fill + submit in one request
curl -s -X POST "$BASE/actions" \
  -H "Content-Type: application/json" \
  -d '{"actions":[
    {"type":"fill","ref":"e3","value":"user@example.com"},
    {"type":"fill","ref":"e5","value":"mypassword"},
    {"type":"click","ref":"e8"}
  ]}'
sleep 2
curl -s "$BASE/instances/$INST/tabs/$TAB/snapshot"
```

---

## 3. Search & Extract

### CLI

```bash
pinchtab nav https://site.com/search
pinchtab snap -i
pinchtab fill e2 "search query"
pinchtab press Enter
sleep 2
pinchtab text                               # extract search results
```

---

## 4. Multi-Tab Workflow

### CLI

```bash
pinchtab tab new https://source.com
pinchtab tab new https://destination.com
pinchtab tab                                # list tabs, note IDs

# Read from source tab
pinchtab tab tab_AAA
DATA=$(pinchtab text)

# Paste into destination tab
pinchtab tab tab_BBB
pinchtab fill e3 "$DATA"
```

### HTTP

```bash
TAB1=$(curl -s -X POST "$BASE/instances/$INST/tabs/open" \
  -H "Content-Type: application/json" -d '{"url":"https://source.com"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

TAB2=$(curl -s -X POST "$BASE/instances/$INST/tabs/open" \
  -H "Content-Type: application/json" -d '{"url":"https://destination.com"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

DATA=$(curl -s "$BASE/instances/$INST/tabs/$TAB1/text" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['text'])")

curl -s -X POST "$BASE/instances/$INST/tabs/$TAB2/action" \
  -H "Content-Type: application/json" -d "{\"type\":\"fill\",\"ref\":\"e3\",\"value\":\"$DATA\"}"
```

---

## 5. Profile Persistence (Session Reuse)

Keep login sessions alive across automation runs.

```bash
# First time: create profile and login
PROF=$(curl -s -X POST "$BASE/profiles" \
  -H "Content-Type: application/json" \
  -d '{"name":"gmail-session","description":"Gmail login"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

INST=$(curl -s -X POST "$BASE/instances/start" \
  -H "Content-Type: application/json" \
  -d "{\"mode\":\"headless\",\"profileId\":\"$PROF\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# Login via automation or headed mode...
# Cookies persist in profile directory

# Later runs: same profile = already logged in
INST=$(curl -s -X POST "$BASE/instances/start" \
  -H "Content-Type: application/json" \
  -d "{\"mode\":\"headless\",\"profileId\":\"$PROF\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
```

---

## 6. Pagination

### CLI

```bash
PAGE=1
while true; do
  echo "=== Page $PAGE ==="
  pinchtab text

  # Find and click next button
  NEXT=$(pinchtab find "next page" 2>/dev/null | head -1)
  [ -z "$NEXT" ] && break

  pinchtab click "$NEXT"
  sleep 2
  PAGE=$((PAGE + 1))
done
```

### HTTP

```bash
PAGE=1
while true; do
  TEXT=$(curl -s "$BASE/instances/$INST/tabs/$TAB/text" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['text'])")
  echo "=== Page $PAGE ==="
  echo "$TEXT"

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

## 7. Stealth Browsing (Anti-Detection)

For sites with bot detection (Cloudflare, reCAPTCHA):

```bash
# Configure stealth before starting instance
pinchtab config set chrome.stealth light    # or "full" for aggressive
pinchtab server &

# Use humanized interactions
pinchtab nav https://protected-site.com
pinchtab snap -i
pinchtab click e3 --humanize
pinchtab fill e5 "data" --humanize
```

---

## 8. JavaScript Extraction

> **Prerequisite**: `security.allowEvaluate` phải bật: `pinchtab config set security.allowEvaluate true`

Extract structured data from pages using JavaScript:

```bash
# Get page title
pinchtab eval "document.title"

# Count links
pinchtab eval "document.querySelectorAll('a').length"

# Extract structured data
pinchtab eval "JSON.stringify(Array.from(document.querySelectorAll('h2')).map(h => h.textContent))"

# HTTP
curl -s -X POST "$BASE/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"expression":"document.querySelectorAll(\"table tr\").length"}'
```

---

## 9. File Download & Upload

> **Prerequisite**: Bật security gates trước khi dùng:
> ```bash
> pinchtab config set security.allowDownload true
> pinchtab config set security.allowUpload true
> ```
> Upload limits mặc định: 5 MB/file, 8 file/request, 10 MB tổng.

```bash
# Download: navigate to page with file link, then download
pinchtab nav https://site.com/downloads
pinchtab snap -i
pinchtab click e5                          # click download link

# Upload file to form
pinchtab nav https://site.com/upload
pinchtab upload "input[type=file]" /path/to/document.pdf
pinchtab click e8                          # submit form
```

---

## 10. Fast Scraping with Blocking

Block images/ads for faster page loads and less bandwidth:

```bash
pinchtab nav https://heavy-site.com --block-images --block-ads
pinchtab text
```

---

## 11. Setup & Teardown Helper

Reusable bash functions for any automation task:

```bash
BASE="http://localhost:9867"

setup_pinchtab() {
  PROF=$(curl -s -X POST "$BASE/profiles" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$1\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
  INST=$(curl -s -X POST "$BASE/instances/start" \
    -H "Content-Type: application/json" \
    -d "{\"mode\":\"headless\",\"profileId\":\"$PROF\"}" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
  TAB=$(curl -s -X POST "$BASE/instances/$INST/tabs/open" \
    -H "Content-Type: application/json" \
    -d "{\"url\":\"$2\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")
  echo "$PROF $INST $TAB"
}

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

## 12. Differential Snapshots (Token-Efficient)

After initial snapshot, use diff mode to get only changed elements:

```bash
# Full snapshot first
pinchtab snap

# After interaction, get only changes
pinchtab click e5
sleep 1
pinchtab snap -d    # diff: only changed elements
```

---

## Tips

- **Always snapshot before interacting** — element refs change when page content changes
- **Add `sleep 1-2`** after navigation/clicks that trigger page loads
- **Prefer `fill` over `type`** for form fields — `fill` clears existing content first
- **Use `text` endpoint** when no interaction needed — saves tokens vs snapshot
- **Use `snap -ic`** for compact interactive-only snapshots
- **Use `snap -d`** after actions to get only changed elements
- **Reuse profiles** for services requiring login — cookies persist
- **Check instances** before creating: `pinchtab instances` or `GET /instances`
- **Block images/ads** for faster loads: `--block-images --block-ads`
- **Use `quick`** for one-shot page analysis: `pinchtab quick <url>`
- **Use batch actions** (`POST /actions`) to reduce request overhead
- **Use stealth** for protected sites: `pinchtab config set chrome.stealth light`
