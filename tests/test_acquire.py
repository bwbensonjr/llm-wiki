"""Tests for the fallback acquisition chain (wiki_ingest.acquire + capture)."""

import datetime
import json
from urllib.parse import quote

import pytest
import requests

from wiki_ingest import acquire, convert, detect
from wiki_ingest.convert import JINA_ENDPOINT, AcquisitionError

from .conftest import FakeResponse

TODAY = datetime.date(2026, 11, 15)

PAPER = (
    "# A Nanopass Framework for Commercial Compiler Development\n\n"
    + "The nanopass framework structures a compiler as many small passes. " * 40
)
STUB_SHELL = (
    "Title: A nanopass framework for commercial compiler development\n\n"
    "Markdown Content:\nReader environment loading\n\nLoading publication (376.9 KB)\n"
)
BOT_CHECK = (
    "Title: Just a moment...\n\nMarkdown Content:\n"
    "## Performing security verification\n"
)


class RoutedSession:
    """URL -> response map; records every request; unknown URLs are 404.

    ``head`` answers with the content type registered for a URL. Entries in
    ``fail`` raise a connection error, like an unreachable host.
    """

    def __init__(self, gets=None, types=None, fail=None):
        self.gets = gets or {}
        self.types = types or {}
        self.fail = set(fail or [])
        self.requests = []

    def head(self, url, **kwargs):
        self.requests.append(("HEAD", url, kwargs))
        if url in self.fail:
            raise requests.ConnectionError(f"unreachable: {url}")
        if url in self.types:
            return FakeResponse(headers={"content-type": self.types[url]})
        return FakeResponse(status_code=404)

    def get(self, url, **kwargs):
        self.requests.append(("GET", url, kwargs))
        if url in self.fail:
            raise requests.ConnectionError(f"unreachable: {url}")
        value = self.gets.get(url)
        if value is None:
            return FakeResponse(status_code=404)
        if isinstance(value, FakeResponse):
            return value
        if isinstance(value, (dict, list)):
            return FakeResponse(text=json.dumps(value))
        return FakeResponse(text=value)

    def urls(self):
        return [url for _, url, _ in self.requests]


@pytest.fixture
def docling(monkeypatch):
    """Docling stand-in: maps a source URL to converted Markdown."""
    outputs = {}

    def fake(source):
        if source in outputs:
            return outputs[source]
        raise convert.ConversionError(f"Docling could not convert source: {source}")

    monkeypatch.setattr(convert, "_convert_docling", fake)
    return outputs


def _capture(tmp_path, source, session, env=None, **kw):
    return convert.capture(
        source,
        raw_dir=tmp_path / "raw",
        session=session,
        today=TODAY,
        env=env or {},
        **kw,
    )


def _front_matter(result):
    return result.raw_path.read_text().split("---", 2)[1]


# --- DOI extraction and URL rewrites ---------------------------------------


@pytest.mark.parametrize(
    "url,doi",
    [
        ("https://doi.org/10.1145/1159803.1159805", "10.1145/1159803.1159805"),
        ("https://dl.acm.org/doi/epdf/10.1145/2544174.2500618", "10.1145/2544174.2500618"),
        ("https://dl.acm.org/doi/10.1145/3386330", "10.1145/3386330"),
        (
            "https://link.springer.com/content/pdf/10.1023/A:1010016816429.pdf",
            "10.1023/A:1010016816429",
        ),
        ("https://example.org/article/10.5555/12345678/", "10.5555/12345678"),
        ("https://example.com/post", None),
    ],
)
def test_extract_doi(url, doi):
    assert acquire.extract_doi(url) == doi


@pytest.mark.parametrize(
    "url,rewritten",
    [
        (
            "https://dl.acm.org/doi/epdf/10.1145/2544174.2500618",
            "https://dl.acm.org/doi/pdf/10.1145/2544174.2500618",
        ),
        (
            "https://dl.acm.org/doi/abs/10.1145/1159803.1159805",
            "https://dl.acm.org/doi/pdf/10.1145/1159803.1159805",
        ),
        ("https://dl.acm.org/doi/pdf/10.1145/3386330", None),
        ("https://arxiv.org/abs/2010.07516", "https://arxiv.org/pdf/2010.07516"),
        ("https://example.com/post", None),
    ],
)
def test_rewrite_url(url, rewritten):
    assert acquire.rewrite_url(url) == rewritten


# --- chain behavior through capture -----------------------------------------

EPDF = "https://dl.acm.org/doi/epdf/10.1145/2544174.2500618"
ACM_PDF = "https://dl.acm.org/doi/pdf/10.1145/2544174.2500618"
DOI = "10.1145/2544174.2500618"
OA_PDF = "https://andykeep.com/pubs/np-preprint.pdf"
TITLE = "A Nanopass Framework for Commercial Compiler Development"


def _openalex(pdf_urls, title=TITLE):
    return {
        "display_name": title,
        "best_oa_location": {"pdf_url": pdf_urls[0]} if pdf_urls else None,
        "locations": [{"pdf_url": u} for u in pdf_urls],
        "open_access": {"oa_url": None},
    }


def test_primary_success_requests_no_fallback(tmp_path):
    session = RoutedSession(
        types={"https://example.com/post": "text/html"},
        gets={JINA_ENDPOINT + "https://example.com/post": "Title: Post\n\nMarkdown Content:\n# Post\n\nBody.\n"},
    )
    result = _capture(tmp_path, "https://example.com/post", session, localize_images=False)
    assert result.acquired_via == "primary"
    assert result.fetched_from is None
    assert "acquired-via: primary" in _front_matter(result)
    assert "fetched-from" not in _front_matter(result)
    assert not any("openalex" in u or "archive.org" in u for u in session.urls())


def test_acm_reader_shell_rewrites_to_pdf(tmp_path, docling):
    docling[ACM_PDF] = PAPER
    session = RoutedSession(
        types={EPDF: "text/html", ACM_PDF: "application/pdf"},
        gets={JINA_ENDPOINT + EPDF: STUB_SHELL},
    )
    result = _capture(tmp_path, EPDF, session)
    assert result.acquired_via == "url-rewrite"
    assert result.source == EPDF
    assert result.fetched_from == ACM_PDF
    fm = _front_matter(result)
    assert f"source: {EPDF}" in fm
    assert f"fetched-from: {ACM_PDF}" in fm
    assert "acquired-via: url-rewrite" in fm
    assert not any("openalex" in u for u in session.urls())


def test_open_access_copy_found_by_doi(tmp_path, docling):
    docling[OA_PDF] = PAPER
    session = RoutedSession(
        types={EPDF: "text/html", ACM_PDF: "text/html", OA_PDF: "application/pdf"},
        gets={
            JINA_ENDPOINT + EPDF: BOT_CHECK,
            JINA_ENDPOINT + ACM_PDF: BOT_CHECK,
            acquire.OPENALEX_ENDPOINT + DOI: _openalex([OA_PDF]),
        },
    )
    result = _capture(tmp_path, EPDF, session)
    assert result.acquired_via == "openalex"
    assert result.source == EPDF
    assert result.fetched_from == OA_PDF
    # No junk twin from the bot-check attempts: exactly one file was written.
    assert [p.name for p in (tmp_path / "raw").glob("*.md")] == [result.raw_path.name]


def test_unpaywall_skipped_without_email(tmp_path, docling):
    session = RoutedSession(
        types={EPDF: "text/html"},
        gets={JINA_ENDPOINT + EPDF: BOT_CHECK, acquire.OPENALEX_ENDPOINT + DOI: _openalex([])},
    )
    with pytest.raises(AcquisitionError):
        _capture(tmp_path, EPDF, session, env={})
    assert not any("unpaywall" in u for u in session.urls())
    assert any(u.startswith(acquire.OPENALEX_ENDPOINT) for u in session.urls())
    # No request carries any identifying data when no email is configured.
    assert not any("email=" in u for u in session.urls())


def test_unpaywall_used_with_email_and_not_recorded(tmp_path, docling):
    docling[OA_PDF] = PAPER
    email = "curator@example.org"
    lookup = f"{acquire.UNPAYWALL_ENDPOINT}{DOI}?email={quote(email)}"
    session = RoutedSession(
        types={EPDF: "text/html", OA_PDF: "application/pdf"},
        gets={
            JINA_ENDPOINT + EPDF: BOT_CHECK,
            acquire.OPENALEX_ENDPOINT + DOI: _openalex([]),
            lookup: {"title": TITLE, "best_oa_location": {"url_for_pdf": OA_PDF}},
        },
    )
    result = _capture(tmp_path, EPDF, session, env={"UNPAYWALL_EMAIL": email})
    assert result.acquired_via == "unpaywall"
    assert email not in result.raw_path.read_text()


def _arxiv_feed(title, arxiv_id="1234.5678v1"):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<feed xmlns="http://www.w3.org/2005/Atom">'
        f"<entry><id>http://arxiv.org/abs/{arxiv_id}</id><title>{title}</title></entry>"
        "</feed>"
    )


def _arxiv_url(title):
    query = quote(f'ti:"{title}"')
    return f"{acquire.ARXIV_ENDPOINT}?search_query={query}&max_results=5"


def test_arxiv_title_match_is_used(tmp_path, docling):
    pdf = "https://arxiv.org/pdf/1234.5678v1"
    docling[pdf] = PAPER
    session = RoutedSession(
        types={EPDF: "text/html", pdf: "application/pdf"},
        gets={
            JINA_ENDPOINT + EPDF: BOT_CHECK,
            acquire.OPENALEX_ENDPOINT + DOI: _openalex([]),
            _arxiv_url(TITLE): _arxiv_feed("A nanopass framework for commercial\n compiler development"),
        },
    )
    result = _capture(tmp_path, EPDF, session)
    assert result.acquired_via == "arxiv"
    assert result.fetched_from == pdf


def test_arxiv_title_mismatch_is_rejected():
    ctx = acquire.Context(source=EPDF, session=RoutedSession(
        gets={_arxiv_url(TITLE): _arxiv_feed("A Different Paper About Compilers")}
    ))
    assert acquire._arxiv(ctx, TITLE) == []
    assert ctx.attempts[-1].outcome == "no preprint with a matching title"


def test_jina_refusal_falls_back_to_direct_fetch(tmp_path):
    url = "https://docs.racket-lang.org/raco/exe.html"
    html = (
        "<html><head><title>raco exe</title></head><body><h1>raco exe</h1>"
        "<p>Creates a standalone executable from a module.</p></body></html>"
    )
    session = RoutedSession(
        types={url: "text/html"},
        gets={
            JINA_ENDPOINT + url: FakeResponse(status_code=403),
            url: FakeResponse(content=html.encode(), headers={"content-type": "text/html"}),
        },
    )
    result = _capture(tmp_path, url, session)
    assert result.acquired_via == "direct"
    assert result.converter == "markitdown"
    assert result.fetched_from is None
    assert "standalone executable" in result.raw_path.read_text()


def test_unreachable_host_falls_back_to_wayback(tmp_path, docling):
    url = "https://legacy.cs.indiana.edu/~dyb/pubs/implicit-phasing.pdf"
    snapshot = acquire.WAYBACK_SNAPSHOT.format(timestamp="20200101000000", url=url)
    docling[snapshot] = PAPER
    availability = acquire.WAYBACK_AVAILABILITY + quote(url, safe="")
    session = RoutedSession(
        fail=[url],
        types={snapshot: "application/pdf"},
        gets={
            availability: {
                "archived_snapshots": {
                    "closest": {"available": True, "status": "200", "timestamp": "20200101000000"}
                }
            }
        },
    )
    result = _capture(tmp_path, url, session)
    assert result.acquired_via == "wayback"
    assert result.source == url
    assert result.fetched_from == snapshot


def test_exhausted_chain_lists_every_attempt(tmp_path, docling):
    session = RoutedSession(
        types={EPDF: "text/html", ACM_PDF: "text/html"},
        gets={
            JINA_ENDPOINT + EPDF: STUB_SHELL,
            JINA_ENDPOINT + ACM_PDF: BOT_CHECK,
            acquire.OPENALEX_ENDPOINT + DOI: _openalex([]),
        },
    )
    with pytest.raises(AcquisitionError) as excinfo:
        _capture(tmp_path, EPDF, session)
    err = excinfo.value
    steps = [a["step"] for a in err.attempts]
    assert steps[0] == "primary"
    for step in ("url-rewrite", "openalex", "arxiv", "direct", "wayback"):
        assert step in steps
    assert err.title == TITLE
    assert not (tmp_path / "raw").exists() or list((tmp_path / "raw").glob("*.md")) == []


def test_bot_check_everywhere_is_reported_not_bypassed(tmp_path):
    session = RoutedSession(
        types={EPDF: "text/html", ACM_PDF: "text/html"},
        gets={JINA_ENDPOINT + EPDF: BOT_CHECK, JINA_ENDPOINT + ACM_PDF: BOT_CHECK},
    )
    with pytest.raises(AcquisitionError) as excinfo:
        _capture(tmp_path, EPDF, session)
    assert "bot check" in str(excinfo.value)


def test_local_file_has_single_candidate(tmp_path):
    missing = tmp_path / "nope.pdf"
    with pytest.raises(detect.DetectionError):
        _capture(tmp_path, str(missing), RoutedSession())


# --- --source-url ------------------------------------------------------------


def test_local_copy_recorded_under_original_url(tmp_path, monkeypatch):
    url = "https://legacy.cs.indiana.edu/~dyb/pubs/implicit-phasing.pdf"
    local = tmp_path / "1291151.1291197.pdf"
    local.write_bytes(b"%PDF-1.4 fake")
    monkeypatch.setattr(
        convert, "_convert_docling", lambda s: "# Implicit Phasing for R6RS Libraries\n\nBody.\n"
    )
    result = _capture(tmp_path, str(local), RoutedSession(), source_url=url)
    fm = _front_matter(result)
    assert f"source: {url}" in fm
    assert f"local-copy: {local}" in fm
    assert "acquired-via: manual" in fm
    assert result.source == url
    assert result.raw_path.name == "2026-11-15-implicit-phasing-for-r6rs-libraries.md"


def test_source_url_requires_local_file(tmp_path):
    with pytest.raises(convert.ConversionError):
        _capture(tmp_path, "https://example.com/x.pdf", RoutedSession(), source_url="https://example.com/y")


def test_local_copy_without_h1_named_from_drop_file(tmp_path, monkeypatch):
    local = tmp_path / "representing-control-in-the-presence-of-first-class-continuations.pdf"
    local.write_bytes(b"%PDF-1.4 fake")
    monkeypatch.setattr(convert, "_convert_docling", lambda s: "## No H1 here\n\nBody.\n")
    result = _capture(
        tmp_path, str(local), RoutedSession(), source_url="https://example.org/papers/rc.pdf"
    )
    assert result.raw_path.name == (
        "2026-11-15-representing-control-in-the-presence-of-first-class-continuations.md"
    )


def test_opaque_local_copy_without_h1_named_from_url(tmp_path, monkeypatch):
    local = tmp_path / "1291151.1291197.pdf"
    local.write_bytes(b"%PDF-1.4 fake")
    monkeypatch.setattr(convert, "_convert_docling", lambda s: "## No H1 here\n\nBody.\n")
    result = _capture(
        tmp_path, str(local), RoutedSession(), source_url="https://example.org/pubs/implicit-phasing.pdf"
    )
    assert result.raw_path.name == "2026-11-15-implicit-phasing.md"
