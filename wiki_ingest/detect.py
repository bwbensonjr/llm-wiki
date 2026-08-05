"""Content-type detection and routing.

Classifies a source as one of four routes. Fetched content type takes
precedence over the file extension, so a URL that resolves to a PDF is routed
to Docling even if its path does not end in `.pdf` — except for a compression
envelope, whose content type describes the wrapper rather than the payload and
so cannot decide a route.
"""

import os
from urllib.parse import urlparse

# Routes / converter names. POSTSCRIPT names both of its stages because this
# value is what a twin's `converter:` field records, and a two-stage conversion
# reported as plain `docling` would misdescribe an immutable artifact.
JINA = "jina"
DOCLING = "docling"
MARKITDOWN = "markitdown"
POSTSCRIPT = "ghostscript+docling"

PDF_EXTENSIONS = {".pdf"}
HTML_EXTENSIONS = {".html", ".htm"}
POSTSCRIPT_EXTENSIONS = {".ps", ".eps"}
GZIP_EXTENSIONS = {".gz"}

# Content types that describe a compression envelope rather than its payload.
# `454.ps.gz` is served as one of these, which says nothing about the PostScript
# inside, so these must not claim a source for the catch-all route.
GZIP_CONTENT_TYPES = {"application/gzip", "application/x-gzip"}

# Some sites reject the default requests User-Agent; present a browser-like one
# so the content-type probe is less likely to be blocked.
PROBE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


class DetectionError(Exception):
    """Raised when a source cannot be reached or classified."""


def is_url(source):
    return urlparse(source).scheme in ("http", "https")


def _strip_gzip(path):
    """Return (inner_path, was_gzipped) for a possibly `.gz`-wrapped path."""
    root, ext = os.path.splitext(path)
    if ext.lower() in GZIP_EXTENSIONS:
        return root, True
    return path, False


def is_postscript_path(path):
    """True for `.ps`/`.eps`, including under a `.gz` wrapper.

    Matching has to look past a compression suffix: `os.path.splitext` on
    `454.ps.gz` yields `.gz`, so a single-extension check misroutes gzipped
    PostScript to the catch-all converter.
    """
    inner, _ = _strip_gzip(path)
    return os.path.splitext(inner)[1].lower() in POSTSCRIPT_EXTENSIONS


def is_gzipped_path(path):
    """True when the path carries a `.gz` compression suffix."""
    return _strip_gzip(path)[1]


def _route_from_extension(path):
    if is_postscript_path(path):
        return POSTSCRIPT
    ext = os.path.splitext(path)[1].lower()
    if ext in PDF_EXTENSIONS:
        return DOCLING
    if ext in HTML_EXTENSIONS:
        return JINA
    return MARKITDOWN


def _url_route_from_extension(path):
    """Route a URL by its path extension when content type is unknown.

    A web URL with no extension (or an `.html`/`.htm` one) is presumed an HTML
    page and routed to Jina Reader; a document-like extension routes normally.
    """
    if is_postscript_path(path):
        return POSTSCRIPT
    ext = os.path.splitext(path)[1].lower()
    if ext in PDF_EXTENSIONS:
        return DOCLING
    if ext and ext not in HTML_EXTENSIONS:
        return MARKITDOWN
    return JINA


def _route_from_content_type(content_type):
    """Map an HTTP content type to a route, or None if uninformative."""
    if not content_type:
        return None
    main = content_type.split(";", 1)[0].strip().lower()
    if "pdf" in main:
        return DOCLING
    if "postscript" in main:
        return POSTSCRIPT
    if main in ("text/html", "application/xhtml+xml"):
        return JINA
    if main in GZIP_CONTENT_TYPES:
        # Uninformative: the type describes the envelope, not what is inside.
        # Returning None defers to the path, which is what recognizes `.ps.gz`.
        return None
    if main:
        return MARKITDOWN
    return None


def detect(source, session=None):
    """Return (route, detected_type) for a source.

    For local paths, route by extension after confirming the file exists.
    For URLs, fetch the content type and let it take precedence over the
    URL's extension, falling back to the extension when the type is absent.
    """
    if is_url(source):
        content_type = _fetch_content_type(source, session=session)
        route = _route_from_content_type(content_type)
        if route is None:
            # Content type is unknown (e.g. the site blocked the probe). Route
            # by the URL's extension, but a web URL with no document-like
            # extension is presumed an HTML page and goes to Jina Reader.
            route = _url_route_from_extension(urlparse(source).path)
        detected = content_type or "web"
        return route, detected

    if not os.path.exists(source):
        raise DetectionError(f"local path does not exist: {source}")
    return _route_from_extension(source), "file"


def _fetch_content_type(url, session=None):
    """Best-effort fetch of the Content-Type header for a URL."""
    import requests

    requester = session or requests
    try:
        resp = requester.head(
            url, allow_redirects=True, timeout=20, headers=PROBE_HEADERS
        )
        if resp.status_code >= 400 or "content-type" not in resp.headers:
            # Some servers reject HEAD; fall back to a ranged GET.
            resp = requester.get(
                url,
                allow_redirects=True,
                timeout=20,
                stream=True,
                headers={**PROBE_HEADERS, "Range": "bytes=0-0"},
            )
            resp.close()
        return resp.headers.get("content-type")
    except requests.RequestException as exc:
        raise DetectionError(f"could not reach source: {url} ({exc})") from exc
