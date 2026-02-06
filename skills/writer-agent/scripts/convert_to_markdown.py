#!/usr/bin/env python3
"""Convert documents to Markdown using Docling.

Usage:
    python convert_to_markdown.py /path/to/file.pdf [output_dir]
    python convert_to_markdown.py /path/to/file.docx docs/generated/lao-tu-tinh-hoa/input-handling
    python convert_to_markdown.py https://example.com/doc.pdf docs/generated/my-book/input-handling

Output: Markdown file in output_dir
    - If output_dir specified: uses that folder
    - If not specified: creates docs/generated/{slug}-{YYMMDD-HHMM}/input-handling/

Note: Writer-agent workflow expects output folders:
    docs/generated/{title}/input-handling/

Supported formats:
    - PDF (text-based and scanned with OCR)
    - DOCX, XLSX, PPTX (Microsoft Office)
    - HTML, Markdown, AsciiDoc
    - EPUB (E-books)
    - Images (PNG, JPEG, TIFF, BMP, WEBP) with OCR

Requires: pip install docling
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Import shared extract_structure module
from extract_structure import extract_structure, generate_slug

# Check EPUB support
try:
    from epub_converter import convert_epub_to_markdown, EPUB_AVAILABLE
except ImportError:
    EPUB_AVAILABLE = False

# Check YouTube support
try:
    from youtube_handler import convert_youtube_to_markdown, is_youtube_url, YOUTUBE_AVAILABLE
except ImportError:
    YOUTUBE_AVAILABLE = False

    def is_youtube_url(url: str) -> bool:
        """Fallback check for YouTube URLs when handler not available."""
        if not url.startswith(("http://", "https://")):
            return False
        return "youtube.com/watch" in url or "youtu.be/" in url

# Check Docling availability
try:
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.datamodel.base_models import InputFormat, ConversionStatus
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False


def get_default_output_dir(input_path: str) -> Path:
    """Generate default output directory following writer-agent convention.

    Pattern: docs/generated/{slug}-{YYMMDD-HHMM}/input-handling/
    """
    input_p = Path(input_path)
    slug = generate_slug(input_p.stem)
    timestamp = datetime.now().strftime("%y%m%d-%H%M")
    return Path("docs/generated") / f"{slug}-{timestamp}" / "input-handling"


def get_output_path(input_path: str, output_dir: Optional[str] = None) -> Path:
    """Generate output markdown path.

    Always outputs as content.md for unified structure.
    """
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = get_default_output_dir(input_path)

    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / "content.md"


def fetch_url_title(url: str) -> Optional[str]:
    """Fetch page title from URL via HTTP request.

    Returns title text or None if failed.
    """
    import re
    try:
        import urllib.request
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; WriterAgent/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            # Read first 50KB to find title (avoid downloading entire page)
            html = response.read(50000).decode("utf-8", errors="ignore")
            # Extract <title> tag content
            match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Clean common suffixes like " - Qiita", " | Medium"
                title = re.split(r"\s*[-|·]\s*(?:Qiita|Medium|GitHub|Dev\.to|Zenn).*$", title, flags=re.IGNORECASE)[0]
                return title.strip()
    except Exception:
        pass
    return None


def extract_title_from_path(source: str) -> str:
    """Extract title from file path or URL.

    For URLs: fetches actual page title.
    For files: converts filename stem to title case.
    Ex: "managing-to-learn.pdf" -> "Managing To Learn"
    """
    if source.startswith(("http://", "https://")):
        # Try to fetch actual page title
        title = fetch_url_title(source)
        if title:
            return title
        # Fallback to URL path stem
        from urllib.parse import urlparse
        parsed = urlparse(source)
        stem = Path(parsed.path).stem or "Document"
    else:
        stem = Path(source).stem

    # Convert kebab-case or snake_case to title
    title = stem.replace("-", " ").replace("_", " ")
    return title.title()


def convert_with_docling(
    source: str,
    output_dir: Optional[str] = None,
    enable_ocr: bool = False,
    enable_tables: bool = False,
    enable_code: bool = False,
    enable_formulas: bool = False,
    enable_picture: bool = False
) -> dict:
    """Convert document to Markdown using Docling.

    Args:
        source: File path or URL
        output_dir: Output directory (default: same as input)
        enable_ocr: Enable OCR for scanned documents
        enable_tables: Enable table structure extraction
        enable_code: Enable code block detection
        enable_formulas: Enable formula/equation extraction

    Returns:
        dict with conversion result
    """
    result = {
        "success": False,
        "source": source,
        "output_path": None,
        "output_dir": None,
        "project_dir": None,
        "structure_path": None,
        "markdown_preview": None,
        "metadata": {},
        "error": None
    }

    # Detect input types
    source_lower = source.lower()
    is_epub = source_lower.endswith('.epub')
    is_youtube = is_youtube_url(source)

    try:
        # YouTube handling (separate from Docling)
        if is_youtube:
            if not YOUTUBE_AVAILABLE:
                result["error"] = "YouTube support requires: uv pip install youtube-transcript-api"
                return result

            markdown_content, yt_metadata = convert_youtube_to_markdown(source)
            doc = None
            epub_title = None
            youtube_title = yt_metadata.get("title", "")

            if yt_metadata.get("warning"):
                result["error"] = yt_metadata["warning"]
                # Still continue - we have content even if just a warning page

        # EPUB handling (separate from Docling)
        elif is_epub:
            if not EPUB_AVAILABLE:
                result["error"] = "EPUB support requires: uv pip install ebooklib beautifulsoup4 lxml"
                return result

            markdown_content, epub_metadata = convert_epub_to_markdown(source)
            # Use EPUB metadata for title if available
            epub_title = epub_metadata.get("title", "")
            youtube_title = None
            doc = None  # No Docling doc for EPUB

        else:
            # Docling handling for other formats
            if not DOCLING_AVAILABLE:
                result["error"] = "Docling not installed. Run: pip install docling"
                return result

            # Configure PDF pipeline options
            pipeline_options = PdfPipelineOptions(
                do_ocr=enable_ocr,
                do_table_structure=enable_tables,
                do_code_enrichment=enable_code,
                do_formula_enrichment=enable_formulas,
                do_picture_classification=enable_picture
            )

            # Initialize converter with options
            converter = DocumentConverter(
                format_options={
                    InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
                }
            )

            # Convert document
            conv_result = converter.convert(source)

            if conv_result.status != ConversionStatus.SUCCESS:
                result["error"] = f"Conversion failed: {conv_result.status}"
                return result

            # Get document and export to markdown
            doc = conv_result.document
            markdown_content = doc.export_to_markdown()
            epub_title = None  # Not EPUB
            youtube_title = None  # Not YouTube

        # Generate output path (unified: always content.md)
        if source.startswith(("http://", "https://")):
            # For URLs, fetch page title for better folder naming
            url_title = fetch_url_title(source)
            if url_title:
                slug = generate_slug(url_title)
            else:
                # Fallback to URL path stem
                from urllib.parse import urlparse
                parsed = urlparse(source)
                slug = generate_slug(Path(parsed.path).stem or "document")

            if output_dir:
                out_dir = Path(output_dir)
            else:
                # Default: docs/generated/{slug}-{timestamp}/input-handling/
                timestamp = datetime.now().strftime("%y%m%d-%H%M")
                out_dir = Path("docs/generated") / f"{slug}-{timestamp}" / "input-handling"
            out_dir.mkdir(parents=True, exist_ok=True)
            output_path = out_dir / "content.md"
        else:
            output_path = get_output_path(source, output_dir)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write markdown file
        output_path.write_text(markdown_content, encoding="utf-8")

        # Extract title from source (use EPUB/YouTube metadata if available)
        if is_youtube and youtube_title:
            title = youtube_title
        elif is_epub and epub_title:
            title = epub_title
        else:
            title = extract_title_from_path(source)

        # Extract structure and write JSON (unified: structure.json)
        structure_path = output_path.with_name("structure.json")
        source_type = "youtube" if is_youtube else "file"
        try:
            structure = extract_structure(markdown_content, source, source_type=source_type, title=title)
            structure_path.write_text(
                json.dumps(structure, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            result["structure_path"] = str(structure_path)
            result["structure"] = structure
        except Exception as struct_err:
            # Structure extraction failed but conversion succeeded
            result["structure_path"] = None
            result["structure_error"] = str(struct_err)

        # Collect metadata (use structure stats if available)
        result["success"] = True
        result["output_path"] = str(output_path)
        result["output_dir"] = str(output_path.parent)
        result["project_dir"] = str(output_path.parent.parent)  # docs/generated/{doc-name}-{timestamp}/
        result["markdown_preview"] = markdown_content[:1000] + "..." if len(markdown_content) > 1000 else markdown_content

        # Use structure stats if available, otherwise calculate
        if "structure" in result:
            stats = result["structure"]["stats"]
            tier_info = result["structure"]["tier_recommendation"]
            result["metadata"] = {
                "char_count": stats["char_count"],
                "word_count": stats["word_count"],
                "line_count": stats["line_count"],
                "tier": tier_info["tier"],
                "heading_count": len(result["structure"]["outline"]),
                "chunk_count": len(result["structure"]["suggested_chunks"]),
                "table_count": len(doc.tables) if doc and hasattr(doc, "tables") else 0,
                "picture_count": len(doc.pictures) if doc and hasattr(doc, "pictures") else 0,
            }
        else:
            result["metadata"] = {
                "char_count": len(markdown_content),
                "word_count": len(markdown_content.split()),
                "line_count": len(markdown_content.splitlines()),
                "table_count": len(doc.tables) if doc and hasattr(doc, "tables") else 0,
                "picture_count": len(doc.pictures) if doc and hasattr(doc, "pictures") else 0,
            }

    except Exception as e:
        result["error"] = f"Conversion error: {str(e)}"

    return result


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: python convert_to_markdown.py <source> [output_dir]"
        }, indent=2))
        sys.exit(1)

    source = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    # Check EPUB first (doesn't require Docling)
    is_epub = source.lower().endswith('.epub')

    if not is_epub and not DOCLING_AVAILABLE:
        print(json.dumps({
            "success": False,
            "error": "Docling not installed. Run: pip install docling"
        }, indent=2))
        sys.exit(2)

    result = convert_with_docling(source, output_dir)
    print(json.dumps(result, indent=2))

    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
