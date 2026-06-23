"""Selective image localization for the web/Jina capture route.

When the `file` command is invoked with image localization enabled, this module
downloads a source's *content* images into the immutable `raw/assets/<twin-stem>/`
layer and rewrites the twin's image links to point at the local copies. It is
mechanical and non-interactive (Phase 1): a source-level opt-in decides *that*
images are kept; a heuristic noise filter decides *which* are content vs. chrome.

Design constraints (see the change `capture-important-images`):

- The rewrite happens before the twin is written, so the raw twin is never
  edited after the fact.
- The assets directory is created only when at least one image is kept, so a
  source with nothing worth keeping leaves no empty directory behind.
- A single image download failure is non-fatal: the link is left as its original
  remote URL and the skip is reported, so one dead URL never aborts a capture.
"""

import mimetypes
import os
import re
from dataclasses import dataclass, field
from urllib.parse import urlparse

# Markdown image: ![alt](src) or ![alt](src "title"). `src` is a single
# whitespace/paren-free token, which covers ordinary and signed URLs. This also
# matches the inner image of a wrapped `[![alt](src)](link)`, leaving the
# wrapping link untouched.
_IMAGE_RE = re.compile(
    r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)(?:\s+\"[^\"]*\")?\)"
)

# Hosts/paths that serve avatars or profile chrome rather than content.
_AVATAR_MARKERS = (
    "avatars.githubusercontent.com",
    "gravatar.com",
    "avatars.",
)

# A small `s=` (size) query value marks an avatar/thumbnail render.
_THUMBNAIL_SIZE_THRESHOLD = 128

# Downloaded payloads below this many bytes are treated as decorative (spacers,
# icons, tracking pixels) and not kept.
MIN_IMAGE_BYTES = 5000

_DOWNLOAD_TIMEOUT = 60


@dataclass
class LocalizeReport:
    """What localization kept and skipped, for the CLI/JSON surface."""

    kept: list = field(default_factory=list)
    skipped: list = field(default_factory=list)

    def as_dict(self):
        return {"kept": self.kept, "skipped": self.skipped}


def find_image_refs(markdown):
    """Return the image references in `markdown` as (alt, src, match) tuples."""
    return [
        (m.group("alt"), m.group("src"), m)
        for m in _IMAGE_RE.finditer(markdown)
    ]


def is_decorative_url(src):
    """Heuristic: True if `src` looks like an avatar/thumbnail, not content."""
    parsed = urlparse(src)
    haystack = (parsed.netloc + parsed.path).lower()
    if any(marker in haystack for marker in _AVATAR_MARKERS):
        return True
    # `s=64`, `s=80`, … are GitHub avatar render sizes; small means chrome.
    for part in parsed.query.split("&"):
        if part.startswith("s="):
            value = part[2:]
            if value.isdigit() and int(value) <= _THUMBNAIL_SIZE_THRESHOLD:
                return True
    return False


def _filename_for(src, index, content_type=None):
    """Stable, legible local filename: `img-<n><ext>` keyed to match order."""
    ext = os.path.splitext(urlparse(src).path)[1].lower()
    if not ext and content_type:
        guessed = mimetypes.guess_extension(content_type.split(";", 1)[0].strip())
        ext = guessed or ""
    return f"img-{index}{ext}"


def _download(src, session=None):
    """Fetch `src`; return (content_bytes, content_type) or raise on failure."""
    import requests

    requester = session or requests
    resp = requester.get(src, timeout=_DOWNLOAD_TIMEOUT)
    resp.raise_for_status()
    return resp.content, resp.headers.get("content-type", "")


def localize(markdown, assets_dir, rel_prefix, session=None):
    """Download content images and rewrite their links to local relative paths.

    Returns (rewritten_markdown, LocalizeReport). `assets_dir` is created lazily
    on the first kept image. Decorative, undersized, and failed-download images
    are left pointing at their original remote URL and recorded as skipped.
    """
    import requests

    from pathlib import Path

    assets_dir = Path(assets_dir)
    report = LocalizeReport()
    # Cache by URL so a content image repeated in the page is fetched once.
    resolved = {}
    counter = 0

    def replace(match):
        nonlocal counter
        counter += 1
        index = counter
        src = match.group("src")

        if src in resolved:
            rel = resolved[src]
            if rel is None:
                return match.group(0)
            return match.group(0).replace(src, rel, 1)

        if is_decorative_url(src):
            resolved[src] = None
            report.skipped.append({"src": src, "reason": "decorative"})
            return match.group(0)

        try:
            content, content_type = _download(src, session=session)
        except requests.RequestException as exc:
            resolved[src] = None
            report.skipped.append({"src": src, "reason": f"download-failed: {exc}"})
            return match.group(0)

        if len(content) < MIN_IMAGE_BYTES:
            resolved[src] = None
            report.skipped.append({"src": src, "reason": "below-size-threshold"})
            return match.group(0)

        assets_dir.mkdir(parents=True, exist_ok=True)
        filename = _filename_for(src, index, content_type)
        (assets_dir / filename).write_bytes(content)
        rel = f"{rel_prefix}/{filename}"
        resolved[src] = rel
        report.kept.append({"src": src, "path": rel})
        return match.group(0).replace(src, rel, 1)

    new_markdown = _IMAGE_RE.sub(replace, markdown)
    return new_markdown, report
