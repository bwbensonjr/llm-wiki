"""Mechanical stub detection, applied to converted Markdown before a twin is written.

A stub is output that converted cleanly but is not the source: a bot-check or
captcha interstitial, an HTTP error page rendered as content, a JavaScript loading
shell, or a "document" far too short to be the paper it claims to be. Because
`raw/` is immutable, such output must be caught here, before the single write;
once written it could never be removed. A stub counts as a failed acquisition
attempt, so the fallback chain moves on to its next candidate.

The checks are deliberately conservative: patterns that only an interstitial or
error page produces, plus a word floor applied only to document routes (PDF and
PostScript), where a paper is expected. HTML pages get no word floor, because a
short but genuine web page is common and the unattended path's own plausibility
judgment is the second line of defense for subtler cases.

Word floor: tuned by running `classify()` over every existing twin in `raw/`;
the shortest genuine document twin is several thousand words, so 150 leaves a wide
margin while still catching a cover page or a loading stub.
"""

import re

from . import detect

DOCUMENT_ROUTES = {detect.DOCLING, detect.POSTSCRIPT}
DOCUMENT_WORD_FLOOR = 150

# Jina Reader's own header warnings. These are the most reliable signals: Jina
# reports the HTTP status it actually received from the target.
_JINA_ERROR_WARNING = re.compile(
    r"^Warning:\s+Target URL returned error (\d{3})", re.MULTILINE
)
_JINA_CAPTCHA_WARNING = re.compile(
    r"^Warning:\s+This page maybe requiring CAPTCHA", re.MULTILINE
)

_BOT_CHECK_PHRASES = (
    "just a moment...",
    "performing security verification",
    "checking your browser before accessing",
    "verify you are human",
    "verifies you are not a bot",
    "enable javascript and cookies to continue",
    "attention required! | cloudflare",
    "ddos protection by",
)

_ERROR_TITLE = re.compile(
    r"\b(page not[- ]found|404 not found|403 forbidden|access denied|"
    r"500 internal server error|service unavailable|not found)\b",
    re.IGNORECASE,
)

_LOADING_SHELL_PHRASES = (
    "you need to enable javascript to run this app",
    "please enable javascript to view",
    "this site requires javascript",
    "loading epdf",
    # ACM's ePDF reader shell: the publication is fetched by script after load.
    "reader environment loading",
    "loading publication (",
)

# Leading Jina header lines, removed before counting words so the header alone
# never makes a stub look substantial.
_JINA_HEADER = re.compile(r"^(Title|URL Source|Warning|Published Time):.*$", re.MULTILINE)


def _title(markdown):
    from .slug import extract_title

    return extract_title(markdown) or ""


def word_count(markdown):
    body = _JINA_HEADER.sub("", markdown)
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)  # images
    body = re.sub(r"\]\([^)]*\)", "]", body)  # link targets
    return len(re.findall(r"[A-Za-z]{2,}", body))


def classify(markdown, route, remote=True):
    """Return a short reason string if ``markdown`` is a stub, else None.

    ``remote`` is False for a local file. The word floor then does not apply: a
    local file was placed deliberately by the curator, who has already judged it
    to be the source, so only the unmistakable interstitial patterns are checked.
    """
    lowered = markdown.lower()
    title = _title(markdown)

    match = _JINA_ERROR_WARNING.search(markdown)
    if match:
        return f"error page (target returned HTTP {match.group(1)})"
    if _JINA_CAPTCHA_WARNING.search(markdown):
        return "bot check or captcha page"
    if any(phrase in lowered for phrase in _BOT_CHECK_PHRASES):
        return "bot check or captcha page"
    if title and _ERROR_TITLE.search(title):
        return f"error page (titled '{title}')"
    words = word_count(markdown)
    if words < 400 and any(p in lowered for p in _LOADING_SHELL_PHRASES):
        return "JavaScript loading shell, no content"
    if remote and route in DOCUMENT_ROUTES and words < DOCUMENT_WORD_FLOOR:
        return f"implausibly thin for a document ({words} words)"
    return None
