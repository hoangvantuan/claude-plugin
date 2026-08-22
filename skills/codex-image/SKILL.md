---
name: codex-image
description: "Generate and edit bitmap images with OpenAI gpt-image-2 (OpenAI API fallback). Supports transparent backgrounds, batch generation, and editing up to 4K."
argument-hint: "[image description] [--size WxH] [--transparent] [--batch N] [--edit input.png]"
---

# Codex Image: image generation via Codex CLI + OpenAI API fallback

Generate and edit images with `gpt-image-2` (default) through two modes.

## Two modes

| Mode | Mechanism | Requirements | When to use |
|---|---|---|---|
| **Default: `codex exec`** | Ask the Codex agent to call the built-in `$imagegen` tool | Codex CLI + ChatGPT login (no API key needed) | Every ordinary request: generate, variations, chroma-key transparency, batch |
| **Fallback: `scripts/image_gen.py`** | Call the OpenAI Image API directly | `OPENAI_API_KEY` + `openai`/`pillow` in the venv | Only when the user explicitly asks for CLI/API/model control, OR the user confirms they need: exact size/quality, high-fidelity/mask edits, native transparency (gpt-image-1.5) |

Mode-switching rules:

- Do not switch to the fallback just because size/quality needs adjusting — hint it inside the prompt first.
- **Never silently drop to `gpt-image-1.5`** — that is a model downgrade; ask the user first (unless they requested it by name).
- The fallback needs `OPENAI_API_KEY`: if it is missing, point the user to https://platform.openai.com/api-keys and have them set the env var themselves — **never ask the user to paste a key into chat**.
- **Do not modify `scripts/image_gen.py`** (vendored from OpenAI, Apache 2.0 — see `scripts/LICENSE.txt`). If something is missing, ask the user.

## When NOT to use this skill

- Icons/logos/UI graphics that must match an SVG/vector set **already in the repo** → edit the vector file directly.
- Simple shapes, diagrams, wireframes → better done code-native with SVG/HTML/CSS.
- An image already in the project in an editable format that needs only a small tweak → edit the source file.

## Environment requirements

```bash
codex --version   # Codex CLI: npm install -g @openai/codex, then run `codex` to log in to ChatGPT
```

The fallback CLI also needs: `uv pip install --python ~/.venv/claude/bin/python openai pillow` and `OPENAI_API_KEY`.

## Workflow

1. **Mode**: `codex exec` by default; fallback only when the user explicitly asks or has confirmed it.
2. **Intent**: user wants a **new** image (even with reference images for style/mood) → generate; wants to **keep most of an existing image** → edit. When unclear, treat it as generate.
3. **Count**: 1 image → 1 command; several distinct assets → 1 command per asset (or `batch-generate.py`); many prompts on the API path → `generate-batch`.
4. **Prompt**: build it with the schema below, applying the augmentation policy.
5. **Run → verify the file exists at the destination** (see Output policy) → inspect the image (subject, style, text, constraints) → iterate one change at a time.
6. **Report**: final path, prompt used, which mode.

## 1. Text-to-image (default path)

```bash
codex exec --skip-git-repo-check --enable image_generation \
  '$imagegen <PROMPT>. Save the final PNG as <FILENAME>.png in <ABSOLUTE_OUTPUT_DIR>.'
```

- The built-in tool only takes prompt text: size, style, and quality must be described inside the prompt ("1024x1024 square format", "wide landscape 1536x1024"). Picking a size: `references/size-guide.md`.
- Example: `'$imagegen A minimal flat-design coffee cup icon, white background, 1024x1024. Save as coffee-icon.png in /path/to/output.'`

## 2. Transparent background

The default path uses chroma-key removal (gpt-image-2 does not support `background=transparent`):

**Step 1 — generate on a chroma-key background.** Append to the prompt (verbatim):

```text
Create the requested subject on a perfectly flat solid #00ff00 chroma-key background for background removal.
The background must be one uniform color with no shadows, gradients, texture, reflections, floor plane, or lighting variation.
Keep the subject fully separated from the background with crisp edges and generous padding.
Do not use #00ff00 anywhere in the subject.
No cast shadow, no contact shadow, no reflection, no watermark, and no text unless explicitly requested.
```

If the subject is green, switch to `#ff00ff` (magenta). Never use a key color that appears in the subject.

**Step 2 — remove the background locally:**

```bash
~/.venv/claude/bin/python skills/codex-image/scripts/remove_chroma_key.py \
  --input <source.png> --out <final.png> \
  --auto-key border --soft-matte \
  --transparent-threshold 12 --opaque-threshold 220 --despill
```

Note on `--despill`: it kills green spill on the edges, but **also strips genuine green from the subject** (verified: green apple leaves turned gray). If the subject contains colors close to the key, drop `--despill`, or better, use a magenta key back in step 1.

**Step 3 — validate**: open the image and look. The output must have an alpha channel, transparent corners, sensible subject coverage, no key-color fringe, and **unaltered subject colors**. Thin fringe remaining → retry once with `--edge-contract 1`; visible jagged edges (subject with no shadow/reflection) → add `--edge-feather 0.25`.

**Escape hatch — native transparency.** If the user needs true transparency, the subject is complex (hair, fur, smoke, glass, liquid, reflective objects, soft shadows), or chroma-key fails validation → explain and **ask the user first** before running the fallback:

```bash
~/.venv/claude/bin/python skills/codex-image/scripts/image_gen.py generate \
  --model gpt-image-1.5 --prompt "<PROMPT>" \
  --background transparent --output-format png --out <final.png>
```

(Needs `OPENAI_API_KEY`; if missing, guide the user through setting it. Last resort with no key: a dedicated tool such as remove.bg or Photoshop.)

## 3. Batch (multiple images)

**Default path** — the script calls `codex exec` sequentially per prompt and names files `prefix-001.png`...:

```bash
~/.venv/claude/bin/python skills/codex-image/scripts/batch-generate.py \
  --prompts "prompt 1" "prompt 2" --output-dir ./output-images/ --prefix batch
# or --prompt-file prompts.txt (one prompt per line)
```

**API path** (only after the user has chosen the fallback) — concurrent runs from JSONL, see `references/cli.md`:

```bash
~/.venv/claude/bin/python skills/codex-image/scripts/image_gen.py generate-batch \
  --input prompts.jsonl --out-dir output/ --concurrency 5
```

Note: the word "batch" in a request does NOT mean switching to the API fallback. Several distinct assets = several separate prompts, not `--n` (n is only for variants of the same prompt).

## 4. Image editing

Route by how much of the original must be preserved:

| Request | Path | Mechanism |
|---|---|---|
| Variations, style transfer, "redraw it like..." | `codex exec -i` (default) | The model looks at the image → re-describes it → generates a new one. Composition holds up reasonably well, but this is NOT pixel-level editing |
| Exact preservation: keep a face/person, remove/replace one object, change the background while keeping the subject, fix in-image text, mask/inpainting | `image_gen.py edit` (fallback, ask first) | The image goes straight to the edit endpoint; gpt-image-2 is always high-fidelity; supports `--mask` |

**Default path** (note: `exec` is required, and the `--` separator keeps the `-i` flag from swallowing the prompt):

```bash
codex exec --skip-git-repo-check --enable image_generation \
  -i <source.png> -- '$imagegen Modify this image: <DESCRIPTION>. Change only X; keep Y unchanged. Save as <output>.png in <directory>.'
```

Multiple reference images: `-i style-ref.png,content-ref.png` — in the prompt, address each image by index and role (Image 1: style reference...).

**API path:**

```bash
~/.venv/claude/bin/python skills/codex-image/scripts/image_gen.py edit \
  --image input.png --prompt "Replace only the background with a warm sunset; keep the subject unchanged" \
  --out edited.png
```

Invariants rule: every edit prompt must spell out `change only X; keep Y unchanged`, and **repeat it on every iteration** to prevent drift.

## 5. Prompt

Schema (use the lines you need; it is not a form to fill in completely):

```text
Use case: <taxonomy slug>
Primary request: <the user's core request>
Subject / Scene: <subject + setting>
Style/medium: <photo/illustration/3D...>
Composition/framing: <wide/close/top-down; placement>
Lighting/mood: <lighting + mood>
Text (verbatim): "<exact text>"
Constraints: <must keep / must avoid>
```

Augmentation policy:

- User prompt **already detailed** → only normalize it into a clean spec, do NOT add creative requirements.
- **Generic** prompt → add measured detail (composition, polish level, plausible setting). Do NOT add characters/objects/brands/slogans that are not implied.
- Missing a key detail that blocks success → ask the user; otherwise proceed.

Use-case taxonomy (slugs): generate — `photorealistic-natural`, `product-mockup`, `ui-mockup`, `infographic-diagram`, `scientific-educational`, `ads-marketing`, `productivity-visual`, `logo-brand`, `illustration-story`, `stylized-concept`, `historical-scene`; edit — `text-localization`, `identity-preserve`, `precise-object-edit`, `lighting-weather`, `background-extraction`, `style-transfer`, `compositing`, `sketch-to-render`.

Full principles: `references/prompting.md`. Copy/paste recipes by use case: `references/sample-prompts.md`.

## Output policy

1. The prompt always states "Save as X.png in <absolute directory>". After `codex exec` finishes, **verify the file exists at the destination**; if it is missing, find the newest image in `~/.codex/generated_images/`, copy it to the destination, and tell the user.
2. **Never leave a project asset sitting only in `~/.codex/generated_images/`**.
3. **Never overwrite an existing file** unless the user explicitly asks — create a versioned name (`hero-v2.png`, `icon-edited.png`).
4. Always close with: final path, prompt used, which mode.

## Common errors

| Error | Cause | Fix |
|---|---|---|
| `codex: command not found` | Codex CLI not installed | `npm install -g @openai/codex` |
| `image_generation is not enabled` | Feature not turned on | Add `--enable image_generation` |
| `Authentication required` | Not logged in | Run `codex` and log in to ChatGPT |
| `No prompt provided via stdin` | The `-i` flag swallowed the prompt | Add `--` before the prompt: `-i img.png -- '$imagegen ...'` |
| Opens the TUI instead of running | Missing `exec` | Use `codex exec ...` |
| File never appears at the destination | Codex saved to its default path | Look in `~/.codex/generated_images/`, copy it over |
| Wrong image size (default path) | The model decides | State the size in the prompt; when it must be exact → fallback `--size` |
| Misspelled text in the image | Prompt not explicit enough | Put text in quotes, spell hard words letter-by-letter |
| Green fringe after background removal | Soft/antialiased edges | Retry with `--edge-contract 1`; too complex → ask about the gpt-image-1.5 fallback |
| Green in the subject turned gray | `--despill` stripped a real color | Rerun without `--despill`, or regenerate on a magenta background |
| `OPENAI_API_KEY` missing (fallback) | Key not set | Guide the user to create the key + set the env var; never paste a key into chat |

## Reference map

- `references/prompting.md` — prompting principles (shared by both modes) + style/composition/lighting vocabulary tables
- `references/sample-prompts.md` — copy/paste recipes by use case (shared by both modes)
- `references/size-guide.md` — size selection by use case + gpt-image-2 constraints
- `references/cli.md` — fallback CLI: commands, flags, quality, mask, batch JSONL (read only when entering fallback)
- `references/image-api.md` — Image API parameters (read only when entering fallback)
- `scripts/image_gen.py` — fallback CLI (vendored from OpenAI Codex, Apache 2.0, do not modify)
- `scripts/remove_chroma_key.py` — chroma-key background removal (vendored from OpenAI Codex, Apache 2.0)
- `scripts/batch-generate.py` — sequential batch on the `codex exec` path
