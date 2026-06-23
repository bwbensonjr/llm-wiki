"""Converter router and raw-twin writer (Phase 1 — capture).

Routes a source to Jina Reader, Docling, or MarkItDown, produces a Markdown
twin in memory, and only then writes it to `raw/<date>-<slug>.md`. Conversion
is all-or-nothing: any failure raises and leaves no file behind.
"""

import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from . import detect
from .slug import twin_slug

JINA_ENDPOINT = "https://r.jina.ai/"


class ConversionError(Exception):
    """Raised when the routed converter cannot produce Markdown."""


@dataclass
class CaptureResult:
    raw_path: Path
    converter: str
    detected_type: str
    title: str
    images: Optional[dict] = None


def _convert_jina(url, session=None):
    import os

    import requests

    requester = session or requests
    # Keyless by default; an optional JINA_API_KEY lifts rate/auth limits.
    headers = {}
    api_key = os.environ.get("JINA_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    try:
        resp = requester.get(JINA_ENDPOINT + url, timeout=120, headers=headers)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise ConversionError(f"Jina Reader request failed: {exc}") from exc
    text = resp.text
    if not text.strip():
        raise ConversionError("Jina Reader returned empty content")
    return text


def _convert_docling(source):
    try:
        from docling.document_converter import DocumentConverter
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise ConversionError(f"docling is not available: {exc}") from exc
    try:
        result = DocumentConverter().convert(source)
        markdown = result.document.export_to_markdown()
    except Exception as exc:
        raise ConversionError(f"Docling could not convert source: {exc}") from exc
    if not markdown.strip():
        raise ConversionError("Docling produced empty Markdown")
    return markdown


def _convert_markitdown(source):
    try:
        from markitdown import MarkItDown
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise ConversionError(f"markitdown is not available: {exc}") from exc
    try:
        result = MarkItDown().convert(source)
        markdown = result.text_content
    except Exception as exc:
        raise ConversionError(
            f"MarkItDown could not convert source: {exc}"
        ) from exc
    if not markdown or not markdown.strip():
        raise ConversionError("MarkItDown produced empty Markdown")
    return markdown


def convert(source, route, session=None):
    """Convert a source to Markdown using the chosen route."""
    if route == detect.JINA:
        return _convert_jina(source, session=session)
    if route == detect.DOCLING:
        return _convert_docling(source)
    if route == detect.MARKITDOWN:
        return _convert_markitdown(source)
    raise ConversionError(f"unknown converter route: {route}")


def _unique_path(raw_dir, date, slug):
    """raw/<date>-<slug>.md, suffixed -2, -3, … to avoid overwriting a twin."""
    base = raw_dir / f"{date}-{slug}.md"
    if not base.exists():
        return base
    n = 2
    while True:
        candidate = raw_dir / f"{date}-{slug}-{n}.md"
        if not candidate.exists():
            return candidate
        n += 1


def capture(source, raw_dir="raw", session=None, today=None, localize_images=True):
    """Run Phase 1: detect, convert, and write the immutable raw twin.

    Returns a CaptureResult. Raises DetectionError or ConversionError before
    writing anything if the source cannot be reached or converted. When
    ``localize_images`` is set (the default) and the source took the Jina route,
    that source's content images are downloaded into ``raw/assets/<twin-stem>/``
    and the twin's links are rewritten to the local copies before the twin is
    written. The mechanical filter is the selectivity control, so a page with no
    content images downloads nothing; pass ``localize_images=False`` to suppress
    localization entirely.
    """
    route, detected_type = detect.detect(source, session=session)
    markdown = convert(source, route, session=session)

    from .slug import extract_title

    title = extract_title(markdown) or twin_slug(source, markdown)
    slug = twin_slug(source, markdown)
    date = (today or datetime.date.today()).isoformat()

    raw_dir = Path(raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    path = _unique_path(raw_dir, date, slug)

    # Localize images only after the twin path (and thus its stem) is known, and
    # only for the Jina route. The rewrite happens before the single twin write,
    # so the immutable twin is never edited after the fact; the assets directory
    # is created lazily by localize() only if an image is actually kept.
    images = None
    if localize_images and route == detect.JINA:
        from .images import localize

        stem = path.stem
        assets_dir = raw_dir / "assets" / stem
        markdown, report = localize(
            markdown, assets_dir, f"assets/{stem}", session=session
        )
        images = report.as_dict()

    front_matter = (
        "---\n"
        f"source: {source}\n"
        f"fetched-at: {date}\n"
        f"converter: {route}\n"
        "---\n\n"
    )
    # Write only after a successful in-memory conversion (all-or-nothing).
    path.write_text(front_matter + markdown, encoding="utf-8")

    return CaptureResult(
        raw_path=path,
        converter=route,
        detected_type=detected_type,
        title=title,
        images=images,
    )
