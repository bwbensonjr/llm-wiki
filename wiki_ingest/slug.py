"""Slug derivation for raw twins.

Slug = title slugified: lowercased, ASCII, spaces and punctuation collapsed to
single hyphens. See CLAUDE.md for the full rule.
"""

import os
import re
import unicodedata
from urllib.parse import unquote, urlparse


def slugify(text):
    """Lowercase ASCII slug; non-alphanumeric runs collapse to single hyphens."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text).strip("-").lower()
    return slug


def extract_title(markdown):
    """Return a human-readable title from converted Markdown, or None.

    Jina Reader emits a structured header whose `Title:` line carries the
    page title, terminated by a `Markdown Content:` marker; its body uses
    lower-level headings, so there is often no `# H1` to find. Read that
    header first (only when the marker is present, so a stray `Title:` in
    ordinary prose is not mistaken for one), then fall back to the first
    Markdown H1 (`# ...`) for Docling/MarkItDown output.
    """
    lines = markdown.splitlines()
    if "Markdown Content:" in markdown:
        for line in lines:
            if line.strip() == "Markdown Content:":
                break
            match = re.match(r"Title:\s+(.+?)\s*$", line)
            if match and match.group(1).strip():
                return match.group(1).strip()
    for line in lines:
        match = re.match(r"#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return None


def fallback_name(source):
    """Derive a name from a URL path segment or local filename."""
    parsed = urlparse(source)
    if parsed.scheme in ("http", "https"):
        path = unquote(parsed.path).rstrip("/")
        segment = path.rsplit("/", 1)[-1] if path else parsed.netloc
        candidate = segment or parsed.netloc
    else:
        candidate = os.path.basename(source.rstrip("/"))
    # Drop a file extension if present.
    candidate = os.path.splitext(candidate)[0]
    return candidate or "untitled"


def twin_slug(source, markdown):
    """Slug for a raw twin: from the extracted title, else a fallback name."""
    title = extract_title(markdown)
    base = title if title else fallback_name(source)
    slug = slugify(base)
    return slug or "untitled"
