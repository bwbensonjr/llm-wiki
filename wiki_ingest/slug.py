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
    """Return the text of the first Markdown H1 (`# ...`), or None."""
    for line in markdown.splitlines():
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
