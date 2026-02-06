#!/usr/bin/env python3
"""Extract document structure from markdown content.

Usage:
    python extract_structure.py <markdown_file> [--source <source>] [--source-type <type>] [--title <title>] [--output <dir>]

Example:
    python extract_structure.py content.md --source "https://example.com" --source-type url --title "My Article"
    python extract_structure.py content.md  # Uses defaults

Output: structure.json in same directory as input or specified output directory
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlparse

# Tier thresholds for context management (word-based)
TIER_1_MAX_WORDS = 50000    # Full content
TIER_2_MAX_WORDS = 100000   # Smart compression
# Above 100K words → Tier 3 (reference-based)

# Target chunk size for suggested_chunks (in words)
TARGET_CHUNK_WORDS = 11500  # Target chunk size for subagent processing

# Overlap settings for chunk continuity
CHUNK_OVERLAP_LINES = 10  # ~100-150 words overlap between chunks

# Critical section detection thresholds
CRITICAL_MIN_WORDS = 500  # Sections with substantial content
CRITICAL_MAX_PERCENT = 30  # Max percentage of sections marked critical

# Keywords that suggest critical content (Vietnamese + English)
CRITICAL_KEYWORDS = [
    # Vietnamese
    "định nghĩa", "khái niệm", "nguyên tắc", "cốt lõi", "quan trọng",
    "kết luận", "tóm tắt", "luận điểm", "triết lý", "tư tưởng",
    # English
    "definition", "concept", "principle", "core", "important",
    "conclusion", "summary", "thesis", "philosophy", "key",
    "overview", "introduction", "fundamental", "essential"
]

# Patterns that suggest critical content (regex)
CRITICAL_PATTERNS = [
    r"```[\s\S]{50,}?```",          # Code blocks (>50 chars)
    r"\|.+\|.+\|[\s\S]*?\|.+\|",    # Tables (at least 2 columns)
    r"(?:^|\n)\d+\.\s+.+(?:\n\d+\.\s+.+){2,}",  # Numbered lists (3+ items)
    r"\*\*[^*]+\*\*\s*[:：]",        # Bold definitions (Term: ...)
]

__all__ = [
    "extract_structure",
    "generate_slug",
    "detect_critical_sections",
    "detect_language",
    "TIER_1_MAX_WORDS",
    "TIER_2_MAX_WORDS",
    "TARGET_CHUNK_WORDS",
    "CHUNK_OVERLAP_LINES",
]


def detect_language(text: str, sample_size: int = 5000) -> str:
    """Detect document language from text sample.

    Returns 'vi' for Vietnamese, 'en' for English, 'mixed' for mixed content.
    Uses Unicode range detection for Vietnamese diacritics.
    """
    sample = text[:sample_size]
    words = sample.split()
    if not words:
        return "mixed"

    # Vietnamese diacritics: characters with combining marks specific to Vietnamese
    vi_pattern = re.compile(
        r'[àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ'
        r'ÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ]'
    )

    vi_word_count = sum(1 for w in words if vi_pattern.search(w))
    vi_ratio = vi_word_count / len(words)

    if vi_ratio > 0.15:
        return "vi"
    elif vi_ratio < 0.03:
        return "en"
    else:
        return "mixed"


def detect_critical_sections(outline: List[Dict[str, Any]], lines: List[str]) -> List[Dict[str, Any]]:
    """Detect and mark potentially critical sections.

    Critical sections are those that:
    - Have substantial word count (>=500 words)
    - Contain keywords suggesting definitions, core concepts, conclusions
    - Have high quote density (many direct quotes)
    - Contain code blocks, tables, or structured data
    - Contain numbered lists (action items, steps)

    Args:
        outline: List of section dicts with line, line_end, word_count
        lines: Original document lines

    Returns:
        Updated outline with 'critical' and 'critical_reason' fields
    """
    if not outline:
        return outline

    # Score each section
    scored = []
    for item in outline:
        score = 0
        reasons = []

        # Check word count
        word_count = item.get("word_count", 0)
        if word_count >= CRITICAL_MIN_WORDS:
            score += 2
            reasons.append(f"substantial ({word_count} words)")

        # Check title for keywords
        title_lower = item.get("text", "").lower()
        for keyword in CRITICAL_KEYWORDS:
            if keyword in title_lower:
                score += 3
                reasons.append(f"keyword: {keyword}")
                break

        # Check content for quote density
        start = item.get("line", 1) - 1
        end = item.get("line_end", start + 1)
        section_text = "\n".join(lines[start:end])
        quote_count = section_text.count('"') // 2  # Rough quote pair count
        if quote_count >= 3:
            score += 2
            reasons.append(f"{quote_count} quotes")

        # Check for definition patterns
        if any(pattern in section_text.lower() for pattern in ["là gì", "được định nghĩa", "có nghĩa là", "refers to", "is defined as"]):
            score += 2
            reasons.append("contains definition")

        # Check for critical patterns (code blocks, tables, numbered lists)
        for pattern in CRITICAL_PATTERNS:
            if re.search(pattern, section_text):
                if "```" in pattern:
                    score += 3
                    reasons.append("code block")
                elif "|" in pattern:
                    score += 2
                    reasons.append("table")
                elif r"\d+" in pattern:
                    score += 2
                    reasons.append("numbered list")
                elif "**" in pattern:
                    score += 1
                    reasons.append("bold definition")
                break

        scored.append((item, score, reasons))

    # Sort by score and mark top 30% as critical
    scored.sort(key=lambda x: x[1], reverse=True)
    max_critical = max(1, int(len(scored) * CRITICAL_MAX_PERCENT / 100))

    critical_count = 0
    for item, score, reasons in scored:
        if score >= 2 and critical_count < max_critical:
            item["critical"] = True
            item["critical_reason"] = ", ".join(reasons[:2])  # Top 2 reasons
            critical_count += 1
        else:
            item["critical"] = False
            item["critical_reason"] = None

    return outline


def generate_slug(text: str) -> str:
    """Generate URL-safe slug from text.

    Args:
        text: Title or URL to convert to slug

    Returns:
        Kebab-case slug suitable for folder names
    """
    if not text:
        return f"doc-{datetime.now().strftime('%y%m%d-%H%M')}"

    # If it's a URL, extract meaningful part
    if text.startswith(("http://", "https://")):
        parsed = urlparse(text)
        # Use domain + path (without extension)
        path = parsed.path.rstrip("/")
        if path:
            text = Path(path).stem or parsed.netloc
        else:
            text = parsed.netloc

    # Convert to slug: lowercase, replace non-alphanumeric with hyphen
    slug = text.lower()
    slug = re.sub(r"[.\s_]+", "-", slug)  # Replace dots/spaces/underscores with hyphen
    slug = re.sub(r"[^\w-]", "", slug)    # Remove remaining special chars
    slug = re.sub(r"-+", "-", slug)       # Collapse multiple hyphens
    slug = slug.strip("-")                # Remove leading/trailing hyphens

    # Add timestamp if slug is too short
    if len(slug) < 3:
        slug = f"doc-{datetime.now().strftime('%y%m%d-%H%M')}"

    return slug


def extract_structure(
    markdown_content: str,
    source: str = "",
    source_type: str = "file",
    title: str = ""
) -> Dict[str, Any]:
    """Extract document structure from markdown content.

    Args:
        markdown_content: Markdown string
        source: Original source path/URL
        source_type: Type of source (file, url, pasted_text)
        title: Document title

    Returns:
        dict with version, source_type, title, stats, tier_recommendation, outline, suggested_chunks
    """
    lines = markdown_content.splitlines()
    line_count = len(lines)
    char_count = len(markdown_content)
    word_count = len(markdown_content.split())

    # Extract headings with line numbers
    outline: List[Dict[str, Any]] = []
    for i, line in enumerate(lines, 1):
        if line.startswith("#"):
            stripped = line.lstrip("#")
            level = len(line) - len(stripped)
            text = stripped.strip()
            if text and level <= 6:
                outline.append({
                    "level": level,
                    "text": text,
                    "line": i
                })

    # Calculate section ranges and actual word counts
    for i, item in enumerate(outline):
        if i + 1 < len(outline):
            item["line_end"] = outline[i + 1]["line"] - 1
        else:
            item["line_end"] = line_count

        # Calculate actual word count for section (not rough estimate)
        section_start = item["line"] - 1  # Convert to 0-indexed
        section_end = item["line_end"]
        section_text = "\n".join(lines[section_start:section_end])
        item["word_count"] = len(section_text.split())

    # Detect and mark critical sections
    outline = detect_critical_sections(outline, lines)

    # Count critical sections for stats
    critical_count = sum(1 for item in outline if item.get("critical"))

    # Detect document language
    language = detect_language(markdown_content)

    # Determine processing tier based on word count
    if word_count < TIER_1_MAX_WORDS:
        tier = 1
        tier_reason = f"Word count {word_count:,} < {TIER_1_MAX_WORDS:,}"
    elif word_count < TIER_2_MAX_WORDS:
        tier = 2
        tier_reason = f"Word count {word_count:,} between {TIER_1_MAX_WORDS:,}-{TIER_2_MAX_WORDS:,}"
    else:
        tier = 3
        tier_reason = f"Word count {word_count:,} >= {TIER_2_MAX_WORDS:,}"

    # Direct Path eligibility check
    # Direct Path: <20K words OR (<50K words AND ≤3 articles)
    # Article count estimated from H2 headings (rough: each H2 group → 1 article)
    h2_count = sum(1 for item in outline if item.get("level") == 2)
    h1_count = sum(1 for item in outline if item.get("level") == 1)
    # Fallback: if no H2, use H1 count; if no headings, estimate from word count
    if h2_count > 0:
        estimated_articles = h2_count
    elif h1_count > 0:
        estimated_articles = h1_count
    else:
        # No headings: estimate ~3000 words per article
        estimated_articles = max(1, word_count // 3000)

    # Language-based capacity limits for Direct Path
    # Model ~200K tokens, reserve 50% output = 100K, 40% buffer = 60K, -3K overhead
    capacity_limits = {
        "en": 44000,     # (60K - 3K) / 1.3 ≈ 44K words
        "vi": 32000,     # (60K - 3K) / 1.8 ≈ 32K words
        "mixed": 38000,  # (60K - 3K) / 1.5 ≈ 38K words
    }
    capacity_limit = capacity_limits.get(language, 38000)

    direct_path_eligible = (
        word_count < 20000 or
        (word_count < TIER_1_MAX_WORDS and estimated_articles <= 3)
    )
    direct_path_capacity_ok = word_count <= capacity_limit

    if direct_path_eligible and not direct_path_capacity_ok:
        direct_path_warning = (
            f"Document ({word_count:,} words) may exceed main agent capacity "
            f"for {language} ({capacity_limit:,} words). Consider Tier 1 with subagents."
        )
    else:
        direct_path_warning = None

    # Generate suggested chunks with overlap support
    chunks: List[Dict[str, Any]] = []
    if outline:
        chunk_id = 0
        current_start = 1
        current_words = 0
        heading_path: List[str] = []
        prev_chunk_end = 0  # Track previous chunk end for overlap

        for item in outline:
            section_words = item.get("word_count", 0)

            # If adding this section exceeds target AND we have content, close chunk
            if current_words + section_words > TARGET_CHUNK_WORDS and current_words > 0:
                chunk_end = item["line"] - 1

                # Calculate overlap from previous chunk
                overlap_start = None
                if chunk_id > 0 and prev_chunk_end > 0:
                    overlap_start = max(1, prev_chunk_end - CHUNK_OVERLAP_LINES + 1)

                chunks.append({
                    "id": chunk_id,
                    "line_start": current_start,
                    "line_end": chunk_end,
                    "word_count": current_words,
                    "heading_path": heading_path.copy(),
                    "overlap_from_prev": overlap_start,  # Lines to include from prev chunk
                })

                prev_chunk_end = chunk_end
                chunk_id += 1
                current_start = item["line"]
                current_words = 0
                heading_path = []

            current_words += section_words

            if item["level"] == 1:
                heading_path = [item["text"]]
            elif item["level"] == 2:
                heading_path = heading_path[:1] + [item["text"]] if heading_path else [item["text"]]

        # Final chunk
        if current_words > 0 or not chunks:
            overlap_start = None
            if chunk_id > 0 and prev_chunk_end > 0:
                overlap_start = max(1, prev_chunk_end - CHUNK_OVERLAP_LINES + 1)

            chunks.append({
                "id": chunk_id,
                "line_start": current_start,
                "line_end": line_count,
                "word_count": current_words if current_words > 0 else word_count,
                "heading_path": heading_path,
                "overlap_from_prev": overlap_start,
            })
    else:
        # No headings: single chunk
        chunks = [{
            "id": 0,
            "line_start": 1,
            "line_end": line_count,
            "word_count": word_count,
            "heading_path": [],
            "overlap_from_prev": None,
        }]

    return {
        "version": "1.2",
        "source_type": source_type,
        "source": "./content.md",
        "original_source": source,
        "title": title,
        "language": language,
        "converted_at": datetime.now().isoformat(),
        "stats": {
            "line_count": line_count,
            "char_count": char_count,
            "word_count": word_count,
            "heading_count": len(outline),
            "critical_count": critical_count,
            "estimated_articles": estimated_articles
        },
        "tier_recommendation": {
            "tier": tier,
            "reason": tier_reason
        },
        "direct_path": {
            "eligible": direct_path_eligible,
            "capacity_ok": direct_path_capacity_ok,
            "capacity_limit": capacity_limit,
            "warning": direct_path_warning
        },
        "outline": outline,
        "suggested_chunks": chunks
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract document structure from markdown content"
    )
    parser.add_argument("markdown_file", help="Path to markdown file")
    parser.add_argument("--source", default="", help="Original source path/URL")
    parser.add_argument("--source-type", default="file", choices=["file", "url", "pasted_text"],
                        help="Type of source")
    parser.add_argument("--title", default="", help="Document title")
    parser.add_argument("--output", "-o", help="Output directory (default: same as input)")

    args = parser.parse_args()

    # Read markdown file
    md_path = Path(args.markdown_file)
    if not md_path.exists():
        print(json.dumps({
            "success": False,
            "error": f"File not found: {args.markdown_file}"
        }, indent=2))
        sys.exit(1)

    markdown_content = md_path.read_text(encoding="utf-8")

    # Set defaults
    source = args.source or str(md_path)
    title = args.title or md_path.stem.replace("-", " ").replace("_", " ").title()

    # Extract structure
    structure = extract_structure(markdown_content, source, args.source_type, title)

    # Determine output path
    if args.output:
        out_dir = Path(args.output)
    else:
        out_dir = md_path.parent

    out_dir.mkdir(parents=True, exist_ok=True)
    structure_path = out_dir / "structure.json"

    # Write structure.json
    structure_path.write_text(
        json.dumps(structure, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    # Output result
    result = {
        "success": True,
        "structure_path": str(structure_path),
        "stats": structure["stats"],
        "tier": structure["tier_recommendation"]["tier"],
        "heading_count": len(structure["outline"]),
        "chunk_count": len(structure["suggested_chunks"])
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
