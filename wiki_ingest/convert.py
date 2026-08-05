"""Converter router and raw-twin writer (Phase 1 — capture).

Routes a source to Jina Reader, Docling, MarkItDown, or ghostscript-then-Docling,
produces a Markdown twin in memory, and only then writes it to
`raw/<date>-<slug>.md`. Conversion is all-or-nothing: any failure raises and
leaves no file behind.
"""

import datetime
import gzip
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from . import detect
from .slug import twin_slug

JINA_ENDPOINT = "https://r.jina.ai/"

# PostScript route. ghostscript is an external system binary rather than a Python
# dependency, so it can be absent on a machine where every other route works.
GHOSTSCRIPT_BINARY = "gs"
POSTSCRIPT_MAGIC = b"%!PS"
GZIP_MAGIC = b"\x1f\x8b"
GHOSTSCRIPT_TIMEOUT = 300

# A source whose fonts are bitmap (PK) fonts carries no `ToUnicode` map, so no PDF
# text extractor can recover characters from it: extraction yields glyph *names*,
# which for TeX-produced documents are `/NNN` decimal character codes. The output
# parses as Markdown but is not prose. Measured on two real papers, the ratio of
# such tokens separates cleanly — 0.02 for a good twin, 0.96 for an unusable one —
# so the threshold sits between with wide margin on both sides.
_GLYPH_CODE_TOKEN = re.compile(r"^(?:/\d{1,3})+$")
GLYPH_CODE_RATIO_LIMIT = 0.25


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


def _read_source_bytes(source, session=None):
    """Return the raw bytes of a local path or URL."""
    if not detect.is_url(source):
        try:
            return Path(source).read_bytes()
        except OSError as exc:
            raise ConversionError(f"could not read source: {exc}") from exc

    import requests

    requester = session or requests
    try:
        resp = requester.get(source, timeout=120, headers=detect.PROBE_HEADERS)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise ConversionError(f"could not download source: {exc}") from exc
    return resp.content


def _convert_postscript(source, session=None):
    """Render PostScript to PDF with ghostscript, then convert that PDF.

    Two-stage by design: PostScript is a page-description language with no
    extractable structure, so rendering it to PDF and delegating means the whole
    route inherits Docling's layout handling instead of growing a second, weaker
    extraction path.
    """
    ghostscript = shutil.which(GHOSTSCRIPT_BINARY)
    if ghostscript is None:
        # Phrased to stand alone: the unattended path writes this into an
        # inbox.md park annotation, where it is all the curator sees.
        raise ConversionError(
            f"ghostscript ({GHOSTSCRIPT_BINARY}) not found on PATH; install it to "
            "capture PostScript sources (e.g. `brew install ghostscript`)"
        )

    data = _read_source_bytes(source, session=session)

    # Decompress on the bytes' own evidence rather than the name: the path drives
    # routing, but the gzip magic is what actually says this needs inflating.
    if data[: len(GZIP_MAGIC)] == GZIP_MAGIC:
        try:
            data = gzip.decompress(data)
        except (OSError, EOFError) as exc:
            raise ConversionError(f"could not decompress source: {exc}") from exc

    if not data.lstrip()[: len(POSTSCRIPT_MAGIC)].startswith(POSTSCRIPT_MAGIC):
        raise ConversionError(
            "source was routed as PostScript but does not begin with "
            f"{POSTSCRIPT_MAGIC.decode()}"
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        ps_path = Path(tmpdir) / "input.ps"
        pdf_path = Path(tmpdir) / "output.pdf"
        ps_path.write_bytes(data)
        # Call `gs` directly rather than the `ps2pdf` shell wrapper, and set
        # -dSAFER explicitly even though modern releases default to it:
        # PostScript is a programming language and this input is untrusted.
        command = [
            ghostscript,
            "-dSAFER",
            "-dNOPAUSE",
            "-dBATCH",
            "-sDEVICE=pdfwrite",
            f"-sOutputFile={pdf_path}",
            str(ps_path),
        ]
        try:
            proc = subprocess.run(
                command, capture_output=True, timeout=GHOSTSCRIPT_TIMEOUT
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise ConversionError(f"ghostscript could not be run: {exc}") from exc
        if proc.returncode != 0:
            stderr = proc.stderr.decode("utf-8", "replace").strip()
            raise ConversionError(
                f"ghostscript exited {proc.returncode}: {stderr[-500:]}"
            )
        if not pdf_path.exists() or pdf_path.stat().st_size == 0:
            raise ConversionError("ghostscript produced no PDF output")
        markdown = _convert_docling(str(pdf_path))

    _reject_unrecoverable_glyph_codes(markdown)
    return markdown


def _glyph_code_ratio(markdown):
    """Fraction of whitespace-separated tokens that are bare `/NNN` glyph codes."""
    tokens = markdown.split()
    if not tokens:
        return 0.0
    coded = sum(1 for token in tokens if _GLYPH_CODE_TOKEN.match(token))
    return coded / len(tokens)


def _reject_unrecoverable_glyph_codes(markdown):
    """Refuse a conversion that produced glyph codes instead of text.

    Old `dvips` output built on bitmap fonts converts to a PDF with no usable text
    encoding, and extraction yields `/65/98/115` where "Abs" belongs. Such a twin
    parses fine and is worthless, and `raw/` is immutable — so this refuses before
    the write rather than leaving something unusable that nothing may repair.
    """
    ratio = _glyph_code_ratio(markdown)
    if ratio > GLYPH_CODE_RATIO_LIMIT:
        raise ConversionError(
            f"converted text is {ratio:.0%} unresolved glyph codes (e.g. `/65/98`), "
            "so the source has no recoverable text layer — its PostScript uses "
            "bitmap fonts. Convert it by hand and queue the result as a local file."
        )


def convert(source, route, session=None):
    """Convert a source to Markdown using the chosen route."""
    if route == detect.JINA:
        return _convert_jina(source, session=session)
    if route == detect.DOCLING:
        return _convert_docling(source)
    if route == detect.POSTSCRIPT:
        return _convert_postscript(source, session=session)
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
