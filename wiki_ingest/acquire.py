"""Fallback acquisition: the ordered candidates capture tries for a URL source.

The routed fetch of the source itself is the `primary` candidate. When it fails or
yields a stub, capture asks this generator for the next candidate, in a fixed
order:

    primary -> url-rewrite -> openalex -> unpaywall -> arxiv -> direct -> wayback

Each step self-selects (a URL rewrite only for known hosts, the open-access steps
only when a DOI can be extracted, `direct` only after a failed Jina primary, and so
on) and the generator is lazy, so a primary success makes no further request.
Every candidate URL then goes through the ordinary content-type router; this module
decides *where* to fetch, never *how* to convert.

Limits (see CLAUDE.md): no step attempts to defeat a bot check or captcha, no
shadow library is ever consulted, and no curator data is sent anywhere except the
contact email an index requires, and only when the curator configured it
(`UNPAYWALL_EMAIL`).
"""

import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Optional
from urllib.parse import quote, unquote, urlparse

from . import detect

PRIMARY = "primary"
URL_REWRITE = "url-rewrite"
OPENALEX = "openalex"
UNPAYWALL = "unpaywall"
ARXIV = "arxiv"
DIRECT = "direct"
WAYBACK = "wayback"
MANUAL = "manual"

OPENALEX_ENDPOINT = "https://api.openalex.org/works/doi:"
UNPAYWALL_ENDPOINT = "https://api.unpaywall.org/v2/"
ARXIV_ENDPOINT = "https://export.arxiv.org/api/query"
WAYBACK_AVAILABILITY = "https://archive.org/wayback/available?url="
WAYBACK_SNAPSHOT = "https://web.archive.org/web/{timestamp}id_/{url}"

LOOKUP_TIMEOUT = 20
MAX_OA_CANDIDATES = 3

_DOI = re.compile(r"(10\.\d{4,9}/[^\s?#]+)")
_ACM_DOI_PATH = re.compile(
    r"^/doi/(?:(?:epdf|abs|full|fullHtml|pdf)/)?(10\.\d{4,9}/.+?)/?$"
)
_ARXIV_ABS = re.compile(r"^/abs/(.+?)/?$")
_ATOM = "{http://www.w3.org/2005/Atom}"


@dataclass
class Candidate:
    url: str
    step: str


@dataclass
class Attempt:
    step: str
    url: str
    outcome: str

    def as_dict(self):
        return {"step": self.step, "url": self.url, "outcome": self.outcome}


@dataclass
class Context:
    """State the generator reads between yields (it is filled in by capture)."""

    source: str
    session: object = None
    env: dict = field(default_factory=dict)
    primary_route: Optional[str] = None
    title: Optional[str] = None
    attempts: List[Attempt] = field(default_factory=list)
    title_from_index: bool = False

    def record(self, candidate, outcome):
        self.attempts.append(Attempt(candidate.step, candidate.url, outcome))

    def learn_title(self, title, from_index=False):
        """Keep the first title seen; an index's metadata title replaces a page's."""
        if not title or not title.strip():
            return
        if not self.title or (from_index and not self.title_from_index):
            self.title = title.strip()
            self.title_from_index = self.title_from_index or from_index

    def tried(self, url):
        return any(a.url == url for a in self.attempts)


def extract_doi(url):
    """Return the DOI embedded in a doi.org or publisher URL, or None."""
    parsed = urlparse(url)
    path = unquote(parsed.path)
    if parsed.netloc.lower() in ("doi.org", "dx.doi.org", "www.doi.org"):
        path = path.lstrip("/")
        return path.rstrip("/") or None
    match = _DOI.search(path)
    if not match:
        return None
    doi = match.group(1).rstrip("/")
    # Publisher PDF paths append the extension to the DOI itself
    # (link.springer.com/content/pdf/10.1023/A:1010016816429.pdf).
    if doi.lower().endswith(".pdf"):
        doi = doi[:-4]
    return doi


def rewrite_url(url):
    """Return the known direct-document form of a publisher URL, or None."""
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    if host.endswith("dl.acm.org"):
        match = _ACM_DOI_PATH.match(unquote(parsed.path))
        if match:
            rewritten = f"https://dl.acm.org/doi/pdf/{match.group(1)}"
            return rewritten if rewritten != url else None
    if host.endswith("arxiv.org"):
        match = _ARXIV_ABS.match(parsed.path)
        if match:
            return f"https://arxiv.org/pdf/{match.group(1)}"
    return None


def normalize_title(title):
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


def _get(ctx, url):
    import requests

    requester = ctx.session or requests
    resp = requester.get(url, timeout=LOOKUP_TIMEOUT, headers=detect.PROBE_HEADERS)
    resp.raise_for_status()
    return resp


def _get_json(ctx, url):
    resp = _get(ctx, url)
    if hasattr(resp, "json"):
        return resp.json()
    return json.loads(resp.text)


def _lookup(ctx, step, url, parse):
    """Run one index lookup; record a failed lookup as an attempt, never raise."""
    import requests

    try:
        return parse(_get_json(ctx, url) if step != ARXIV else _get(ctx, url).text)
    except (requests.RequestException, ValueError, ET.ParseError) as exc:
        ctx.attempts.append(Attempt(step, url, f"lookup failed: {exc}"))
    return []


def _openalex(ctx, doi):
    def parse(work):
        ctx.learn_title(work.get("display_name") or work.get("title"), from_index=True)
        urls = []
        best = work.get("best_oa_location") or {}
        for loc in [best] + list(work.get("locations") or []):
            pdf = (loc or {}).get("pdf_url")
            if pdf and pdf not in urls:
                urls.append(pdf)
        oa_url = (work.get("open_access") or {}).get("oa_url")
        if oa_url and oa_url.lower().endswith(".pdf") and oa_url not in urls:
            urls.append(oa_url)
        if not urls:
            ctx.attempts.append(
                Attempt(OPENALEX, OPENALEX_ENDPOINT + doi, "no open-access PDF listed")
            )
        return urls

    return _lookup(ctx, OPENALEX, OPENALEX_ENDPOINT + doi, parse)


def _unpaywall(ctx, doi, email):
    quoted_doi = quote(doi, safe="/:")
    url = f"{UNPAYWALL_ENDPOINT}{quoted_doi}?email={quote(email)}"

    def parse(record):
        ctx.learn_title(record.get("title"), from_index=True)
        urls = []
        best = record.get("best_oa_location") or {}
        for loc in [best] + list(record.get("oa_locations") or []):
            pdf = (loc or {}).get("url_for_pdf")
            if pdf and pdf not in urls:
                urls.append(pdf)
        if not urls:
            ctx.attempts.append(
                Attempt(UNPAYWALL, UNPAYWALL_ENDPOINT + doi, "no open-access PDF listed")
            )
        return urls

    # The recorded attempt URL omits the email so it never reaches inbox.md.
    found = _lookup(ctx, UNPAYWALL, url, parse)
    for attempt in ctx.attempts:
        if attempt.url == url:
            attempt.url = UNPAYWALL_ENDPOINT + doi
    return found


def _arxiv(ctx, title):
    query = quote(f'ti:"{title}"')
    url = f"{ARXIV_ENDPOINT}?search_query={query}&max_results=5"
    wanted = normalize_title(title)

    def parse(text):
        root = ET.fromstring(text)
        for entry in root.iter(f"{_ATOM}entry"):
            entry_title = entry.findtext(f"{_ATOM}title") or ""
            entry_id = entry.findtext(f"{_ATOM}id") or ""
            if normalize_title(entry_title) == wanted and "/abs/" in entry_id:
                return [entry_id.replace("/abs/", "/pdf/", 1).replace("http://", "https://", 1)]
        ctx.attempts.append(Attempt(ARXIV, url, "no preprint with a matching title"))
        return []

    return _lookup(ctx, ARXIV, url, parse)


def _wayback(ctx, url):
    lookup = WAYBACK_AVAILABILITY + quote(url, safe="")

    def parse(data):
        closest = ((data or {}).get("archived_snapshots") or {}).get("closest") or {}
        if closest.get("available") and str(closest.get("status", "200")) == "200":
            timestamp = closest.get("timestamp")
            if timestamp:
                return [WAYBACK_SNAPSHOT.format(timestamp=timestamp, url=url)]
        ctx.attempts.append(Attempt(WAYBACK, lookup, "no archived snapshot"))
        return []

    return _lookup(ctx, WAYBACK, lookup, parse)


def _fresh(ctx, step, urls, limit=None):
    """Yield candidates for ``urls`` not tried yet; record each repeat as skipped.

    An index often lists the very URL an earlier step already fetched (OpenAlex
    commonly offers the publisher PDF the URL rewrite just tried). Recording the
    skip keeps the attempt list complete, so a park annotation shows that the step
    ran and why it fetched nothing, rather than omitting it.
    """
    yielded = 0
    for url in urls:
        earlier = next((a for a in ctx.attempts if a.url == url), None)
        if earlier is not None:
            ctx.attempts.append(
                Attempt(step, url, f"skipped: same URL already tried by {earlier.step}")
            )
            continue
        if limit is not None and yielded >= limit:
            break
        yielded += 1
        yield Candidate(url, step)


def candidates(ctx):
    """Yield acquisition candidates for ``ctx.source`` lazily, in chain order."""
    source = ctx.source
    yield Candidate(source, PRIMARY)

    # Local files and YouTube videos have exactly one way to be captured.
    if not detect.is_url(source) or ctx.primary_route == detect.YOUTUBE:
        return

    rewritten = rewrite_url(source)
    if rewritten:
        yield from _fresh(ctx, URL_REWRITE, [rewritten])

    doi = extract_doi(source)
    if doi:
        yield from _fresh(ctx, OPENALEX, _openalex(ctx, doi), MAX_OA_CANDIDATES)
        email = (ctx.env or {}).get("UNPAYWALL_EMAIL")
        if email:
            yield from _fresh(
                ctx, UNPAYWALL, _unpaywall(ctx, doi, email), MAX_OA_CANDIDATES
            )
        if ctx.title:
            yield from _fresh(ctx, ARXIV, _arxiv(ctx, ctx.title))

    if ctx.primary_route == detect.JINA:
        yield Candidate(source, DIRECT)

    yield from _fresh(ctx, WAYBACK, _wayback(ctx, source))
