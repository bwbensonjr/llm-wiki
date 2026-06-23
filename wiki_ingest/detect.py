"""Content-type detection and routing.

Classifies a source as one of three routes. Fetched content type takes
precedence over the file extension, so a URL that resolves to a PDF is routed
to Docling even if its path does not end in `.pdf`.
"""

import os
from urllib.parse import urlparse

# Routes / converter names.
JINA = "jina"
DOCLING = "docling"
MARKITDOWN = "markitdown"

PDF_EXTENSIONS = {".pdf"}
HTML_EXTENSIONS = {".html", ".htm"}

# Some sites reject the default requests User-Agent; present a browser-like one
# so the content-type probe is less likely to be blocked.
_PROBE_HEADERS = {
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


def _route_from_extension(path):
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
    if main in ("text/html", "application/xhtml+xml"):
        return JINA
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
            url, allow_redirects=True, timeout=20, headers=_PROBE_HEADERS
        )
        if resp.status_code >= 400 or "content-type" not in resp.headers:
            # Some servers reject HEAD; fall back to a ranged GET.
            resp = requester.get(
                url,
                allow_redirects=True,
                timeout=20,
                stream=True,
                headers={**_PROBE_HEADERS, "Range": "bytes=0-0"},
            )
            resp.close()
        return resp.headers.get("content-type")
    except requests.RequestException as exc:
        raise DetectionError(f"could not reach source: {url} ({exc})") from exc
