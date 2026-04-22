#!/usr/bin/env python3
"""Convert EPUB files to Markdown.

Usage:
    python epub_converter.py /path/to/book.epub [output_dir]

Output: Markdown content with preserved heading structure.

Requires: pip install ebooklib beautifulsoup4 lxml
"""
from __future__ import annotations

import re
import warnings
from pathlib import Path
from typing import Optional

# Check EPUB dependencies
try:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup, NavigableString, Tag, XMLParsedAsHTMLWarning
    # Suppress warning when parsing EPUB XML content with HTML parser
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
    EPUB_AVAILABLE = True
except ImportError:
    EPUB_AVAILABLE = False

__all__ = ["convert_epub_to_markdown", "EPUB_AVAILABLE"]


def _get_metadata(book: "epub.EpubBook", field: str) -> Optional[str]:
    """Extract Dublin Core metadata from EPUB."""
    try:
        data = book.get_metadata("DC", field)
        if data and len(data) > 0:
            return data[0][0]
    except (IndexError, KeyError):
        pass
    return None


def _html_to_markdown(soup: "BeautifulSoup") -> str:
    """Convert BeautifulSoup HTML to Markdown.

    Handles: headings, paragraphs, lists, blockquotes, links, images, emphasis.
    """
    lines = []

    # Find body or use whole soup
    body = soup.find("body") or soup

    for element in body.children:
        if isinstance(element, NavigableString):
            text = str(element).strip()
            if text:
                lines.append(text)
            continue

        if not isinstance(element, Tag):
            continue

        tag_name = element.name.lower()

        # Headings
        if tag_name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag_name[1])
            text = element.get_text(strip=True)
            if text:
                lines.append(f"{'#' * level} {text}")
                lines.append("")

        # Paragraphs
        elif tag_name == "p":
            text = _process_inline(element)
            if text:
                lines.append(text)
                lines.append("")

        # Blockquotes
        elif tag_name == "blockquote":
            text = element.get_text(strip=True)
            if text:
                # Handle multi-line blockquotes
                for line in text.split("\n"):
                    lines.append(f"> {line.strip()}")
                lines.append("")

        # Unordered lists
        elif tag_name == "ul":
            for li in element.find_all("li", recursive=False):
                text = _process_inline(li)
                if text:
                    lines.append(f"- {text}")
            lines.append("")

        # Ordered lists
        elif tag_name == "ol":
            for i, li in enumerate(element.find_all("li", recursive=False), 1):
                text = _process_inline(li)
                if text:
                    lines.append(f"{i}. {text}")
            lines.append("")

        # Preformatted/code blocks
        elif tag_name == "pre":
            code = element.get_text()
            lines.append("```")
            lines.append(code.strip())
            lines.append("```")
            lines.append("")

        # Divs and sections - recurse
        elif tag_name in ("div", "section", "article", "aside", "main", "nav"):
            inner = _html_to_markdown(element)
            if inner.strip():
                lines.append(inner)

        # Images
        elif tag_name == "img":
            src = element.get("src", "")
            alt = element.get("alt", "image")
            if src:
                lines.append(f"![{alt}]({src})")
                lines.append("")

        # Horizontal rules
        elif tag_name == "hr":
            lines.append("---")
            lines.append("")

        # Tables - basic support
        elif tag_name == "table":
            table_md = _convert_table(element)
            if table_md:
                lines.append(table_md)
                lines.append("")

    return "\n".join(lines)


def _process_inline(element: "Tag") -> str:
    """Process inline elements (bold, italic, links) within a tag."""
    parts = []

    for child in element.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif isinstance(child, Tag):
            tag = child.name.lower()
            text = child.get_text()

            if tag in ("strong", "b"):
                parts.append(f"**{text}**")
            elif tag in ("em", "i"):
                parts.append(f"*{text}*")
            elif tag == "code":
                parts.append(f"`{text}`")
            elif tag == "a":
                href = child.get("href", "")
                if href and not href.startswith("#"):
                    parts.append(f"[{text}]({href})")
                else:
                    parts.append(text)
            elif tag == "br":
                parts.append("\n")
            elif tag == "span":
                parts.append(_process_inline(child))
            else:
                parts.append(text)

    result = "".join(parts)
    # Clean up whitespace
    result = re.sub(r"\s+", " ", result)
    return result.strip()


def _convert_table(table: "Tag") -> str:
    """Convert HTML table to Markdown table."""
    rows = []

    # Header
    thead = table.find("thead")
    if thead:
        header_row = thead.find("tr")
        if header_row:
            cells = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]
            if cells:
                rows.append("| " + " | ".join(cells) + " |")
                rows.append("| " + " | ".join(["---"] * len(cells)) + " |")

    # Body
    tbody = table.find("tbody") or table
    for tr in tbody.find_all("tr"):
        # Skip header row if no thead
        if not thead and tr.find("th"):
            cells = [th.get_text(strip=True) for th in tr.find_all(["th", "td"])]
            if cells:
                rows.append("| " + " | ".join(cells) + " |")
                rows.append("| " + " | ".join(["---"] * len(cells)) + " |")
            continue

        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append("| " + " | ".join(cells) + " |")

    return "\n".join(rows) if rows else ""


def convert_epub_to_markdown(epub_path: str) -> tuple[str, dict]:
    """Convert EPUB file to Markdown.

    Args:
        epub_path: Path to EPUB file

    Returns:
        tuple[str, dict]: (markdown_content, metadata)
            metadata contains: title, author, language, description

    Raises:
        ImportError: If ebooklib/beautifulsoup4 not installed
        FileNotFoundError: If EPUB file not found
        Exception: If EPUB parsing fails
    """
    if not EPUB_AVAILABLE:
        raise ImportError("EPUB support requires: uv pip install ebooklib beautifulsoup4 lxml")

    path = Path(epub_path)
    if not path.exists():
        raise FileNotFoundError(f"EPUB file not found: {epub_path}")

    # Read EPUB
    book = epub.read_epub(str(path))

    # Extract metadata
    metadata = {
        "title": _get_metadata(book, "title") or path.stem,
        "author": _get_metadata(book, "creator") or "Unknown",
        "language": _get_metadata(book, "language") or "en",
        "description": _get_metadata(book, "description") or "",
        "publisher": _get_metadata(book, "publisher") or "",
        "date": _get_metadata(book, "date") or "",
    }

    # Get spine order (reading order)
    spine_ids = [item[0] for item in book.spine]

    # Map id to item
    items_by_id = {item.id: item for item in book.get_items()}

    # Process chapters in spine order
    markdown_parts = []

    for spine_id in spine_ids:
        item = items_by_id.get(spine_id)
        if item is None:
            continue

        # Only process document items (XHTML)
        if item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue

        try:
            content = item.get_content()
            if not content:
                continue

            # Decode if bytes
            if isinstance(content, bytes):
                content = content.decode("utf-8", errors="ignore")

            # Parse HTML
            soup = BeautifulSoup(content, "lxml")

            # Convert to markdown
            md = _html_to_markdown(soup)
            if md.strip():
                markdown_parts.append(md)

        except Exception:
            # Skip problematic chapters
            continue

    # Join chapters with separator
    markdown_content = "\n\n---\n\n".join(markdown_parts)

    # Add title as H1 if not present
    if markdown_content and not markdown_content.strip().startswith("# "):
        markdown_content = f"# {metadata['title']}\n\n{markdown_content}"

    return markdown_content, metadata


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        print("Usage: python epub_converter.py <epub_file>")
        sys.exit(1)

    if not EPUB_AVAILABLE:
        print("Error: EPUB support requires: uv pip install ebooklib beautifulsoup4 lxml")
        sys.exit(2)

    epub_file = sys.argv[1]

    try:
        content, meta = convert_epub_to_markdown(epub_file)
        print(f"Title: {meta['title']}")
        print(f"Author: {meta['author']}")
        print(f"Language: {meta['language']}")
        print(f"Content length: {len(content)} chars")
        print("\n--- Preview (first 500 chars) ---\n")
        print(content[:500])
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, indent=2))
        sys.exit(1)
