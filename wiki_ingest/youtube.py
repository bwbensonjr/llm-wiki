"""YouTube route: video-ID parsing, metadata and transcript fetch, twin rendering.

A YouTube watch page is served as `text/html`, so the content-type router would
hand it to Jina Reader and file the video's description instead of what is said
in it. This route is recognized by host before any probe, reads the captions,
and refuses to write a twin when there is no transcript to put in it.

Metadata comes from yt-dlp (no download) and captions from
youtube-transcript-api. Both are wrapped in thin functions here so tests can
replace them without touching the network.
"""

import datetime
import html
import re
from dataclasses import dataclass, field
from typing import List, Optional
from urllib.parse import parse_qs, urlparse

from .convert import ConversionError

YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
}

CANONICAL_WATCH_URL = "https://www.youtube.com/watch?v={}"

_VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
# Path forms that carry the ID as the segment after the prefix.
_PATH_PREFIXES = ("shorts", "embed", "live", "v")

# Transcript paragraphs break at the first segment boundary once a paragraph
# spans this long. Auto-generated captions carry no sentence punctuation, so
# time is the only reliable grouping signal.
PARAGRAPH_SECONDS = 60.0

ENGLISH = "en"


def is_youtube_url(source):
    """True when the source is an http(s) URL on a recognized YouTube host."""
    parsed = urlparse(source)
    if parsed.scheme not in ("http", "https"):
        return False
    return (parsed.hostname or "").lower() in YOUTUBE_HOSTS


def video_id(url):
    """Return the 11-character video ID a YouTube URL names, or None.

    Only the ID decides the video: `si`, `t`, `list`, `index`, and any other
    query parameter are ignored, so a playlist-context watch URL captures just
    the one video.
    """
    if not is_youtube_url(url):
        return None
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    segments = [s for s in parsed.path.split("/") if s]

    candidate = None
    if host == "youtu.be":
        candidate = segments[0] if segments else None
    elif segments and segments[0] == "watch":
        candidate = (parse_qs(parsed.query).get("v") or [None])[0]
    elif len(segments) >= 2 and segments[0] in _PATH_PREFIXES:
        candidate = segments[1]

    if candidate and _VIDEO_ID.match(candidate):
        return candidate
    return None


def canonical_url(vid):
    return CANONICAL_WATCH_URL.format(vid)


def canonical_source(source):
    """The form a source is recorded under in `source:`.

    A YouTube video URL collapses to its canonical watch URL; anything else,
    including a YouTube URL that names no video, is returned unchanged.
    """
    vid = video_id(source)
    return canonical_url(vid) if vid else source


# --- fetched data ------------------------------------------------------------


@dataclass
class Chapter:
    title: str
    start: float


@dataclass
class Metadata:
    title: str
    channel: str
    upload_date: Optional[str]  # YYYY-MM-DD
    duration: Optional[float]  # seconds
    description: str
    chapters: List[Chapter] = field(default_factory=list)
    language: Optional[str] = None
    live_status: Optional[str] = None
    availability: Optional[str] = None


@dataclass
class Segment:
    text: str
    start: float


@dataclass
class Transcript:
    language: str
    language_code: str
    is_generated: bool
    segments: List[Segment]


def _unavailable(vid, why):
    return ConversionError(
        f"YouTube video {vid} is unavailable ({why}); nothing captured"
    )


def _blocked(vid, detail):
    return ConversionError(
        f"YouTube refused the request for video {vid} ({detail}); this is "
        "usually IP blocking or rate limiting, not a missing transcript - retry "
        "later or from a different network; nothing captured"
    )


def _no_transcript(vid, why):
    return ConversionError(
        f"YouTube video {vid} has no transcript ({why}); nothing captured"
    )


def _classify_ytdlp_error(vid, message):
    text = message.lower()
    if "not a bot" in text or "429" in text or "too many requests" in text:
        return _blocked(vid, "yt-dlp: sign-in or rate-limit challenge")
    if "live event will begin" in text or "premieres in" in text:
        return ConversionError(
            f"YouTube video {vid} is still live or upcoming; capture it after it "
            "ends; nothing captured"
        )
    if "private" in text:
        return _unavailable(vid, "private")
    if "members" in text:
        return _unavailable(vid, "members-only")
    if "confirm your age" in text or "age-restricted" in text:
        return _unavailable(vid, "age-gated")
    if "removed" in text or "unavailable" in text or "terminated" in text:
        return _unavailable(vid, "removed or unavailable")
    return ConversionError(
        f"could not read metadata for YouTube video {vid}: {message}"
    )


class _SilentLogger:
    """Swallow yt-dlp's own output.

    yt-dlp prints `ERROR: ...` to stderr even with `quiet`, which would break the
    CLI's contract that stderr carries a single JSON error object. The same text
    still arrives in the raised DownloadError, which is classified below.
    """

    def debug(self, msg):
        pass

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


def _extract_info(url):
    """Call yt-dlp for metadata only. Isolated so tests can replace it."""
    import yt_dlp

    options: dict = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
        "logger": _SilentLogger(),
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        return ydl.extract_info(url, download=False)


def _iso_date(yyyymmdd):
    if not yyyymmdd or len(yyyymmdd) != 8:
        return None
    try:
        return datetime.datetime.strptime(yyyymmdd, "%Y%m%d").date().isoformat()
    except ValueError:
        return None


def fetch_metadata(vid):
    """Return Metadata for a video, or raise ConversionError naming the cause."""
    try:
        from yt_dlp.utils import DownloadError
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise ConversionError(f"yt-dlp is not available: {exc}") from exc

    try:
        info = _extract_info(canonical_url(vid))
    except DownloadError as exc:
        raise _classify_ytdlp_error(vid, str(exc)) from exc

    availability = info.get("availability")
    if availability in ("private", "premium_only", "subscriber_only", "needs_auth"):
        raise _unavailable(vid, availability.replace("_", "-"))

    chapters = [
        Chapter(title=(c.get("title") or "").strip(), start=float(c.get("start_time") or 0))
        for c in (info.get("chapters") or [])
    ]
    return Metadata(
        title=(info.get("title") or "").strip(),
        channel=(info.get("channel") or info.get("uploader") or "").strip(),
        upload_date=_iso_date(info.get("upload_date")),
        duration=info.get("duration"),
        description=(info.get("description") or "").strip(),
        chapters=chapters,
        language=info.get("language"),
        live_status=info.get("live_status"),
        availability=availability,
    )


def _list_transcripts(vid):
    """Return youtube-transcript-api's TranscriptList. Isolated for tests."""
    from youtube_transcript_api import YouTubeTranscriptApi

    return YouTubeTranscriptApi().list(vid)


def _base_language(code):
    return (code or "").split("-", 1)[0].lower()


def select_transcript(available, original_language):
    """Pick one transcript in the spec's order, never translating.

    Order: authored English, generated English, authored original-language,
    generated original-language. When the original language is unknown it
    falls back to the first listed authored transcript, then the first
    generated one. Returns None when nothing qualifies.
    """
    available = list(available)
    authored = [t for t in available if not t.is_generated]
    generated = [t for t in available if t.is_generated]

    def first(pool, language):
        return next(
            (t for t in pool if _base_language(t.language_code) == language), None
        )

    original = _base_language(original_language)
    if not original:
        source = authored[0] if authored else (generated[0] if generated else None)
        original = _base_language(source.language_code) if source else ""

    for pool, language in (
        (authored, ENGLISH),
        (generated, ENGLISH),
        (authored, original),
        (generated, original),
    ):
        if language:
            chosen = first(pool, language)
            if chosen is not None:
                return chosen
    return None


def fetch_transcript(vid, original_language):
    """Return the selected Transcript, or raise ConversionError naming the cause."""
    try:
        import youtube_transcript_api as yta
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise ConversionError(
            f"youtube-transcript-api is not available: {exc}"
        ) from exc

    try:
        listing = _list_transcripts(vid)
        chosen = select_transcript(listing, original_language)
        if chosen is None:
            raise _no_transcript(vid, "no captions in English or the video's language")
        fetched = chosen.fetch()
    except ConversionError:
        raise
    except (yta.RequestBlocked, yta.IpBlocked, yta.PoTokenRequired) as exc:
        raise _blocked(vid, type(exc).__name__) from exc
    except yta.TranscriptsDisabled as exc:
        raise _no_transcript(vid, "captions disabled") from exc
    except yta.NoTranscriptFound as exc:
        raise _no_transcript(vid, "no captions found") from exc
    except yta.AgeRestricted as exc:
        raise _unavailable(vid, "age-gated") from exc
    except (yta.VideoUnavailable, yta.VideoUnplayable, yta.InvalidVideoId) as exc:
        raise _unavailable(vid, type(exc).__name__) from exc
    except yta.CouldNotRetrieveTranscript as exc:
        raise ConversionError(
            f"could not retrieve transcript for YouTube video {vid}: "
            f"{type(exc).__name__}; nothing captured"
        ) from exc

    segments = [
        Segment(text=s.text, start=float(s.start)) for s in fetched
    ]
    if not any(s.text.strip() for s in segments):
        raise _no_transcript(vid, "the selected captions are empty")
    # The library names generated tracks "English (auto-generated)"; the kind is
    # recorded separately, so keep only the language name.
    language = re.sub(r"\s*\(auto-generated\)\s*$", "", chosen.language or "")
    return Transcript(
        language=language or chosen.language_code,
        language_code=chosen.language_code,
        is_generated=chosen.is_generated,
        segments=segments,
    )


# --- rendering ---------------------------------------------------------------


def format_timestamp(seconds, long_form):
    total = int(seconds)
    hours, rest = divmod(total, 3600)
    minutes, secs = divmod(rest, 60)
    if long_form:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def _clean(text):
    return " ".join(html.unescape(text).split())


def _paragraphs(segments, long_form):
    """Group segments into timestamped paragraphs of about PARAGRAPH_SECONDS."""
    out = []
    start = None
    words = []
    for seg in segments:
        text = _clean(seg.text)
        if not text:
            continue
        if start is None:
            start = seg.start
        elif seg.start - start >= PARAGRAPH_SECONDS:
            out.append(f"[{format_timestamp(start, long_form)}] {' '.join(words)}")
            start, words = seg.start, []
        words.append(text)
    if words:
        out.append(f"[{format_timestamp(start, long_form)}] {' '.join(words)}")
    return out


def _by_chapter(segments, chapters):
    """Yield (chapter_title, segments) in chapter order.

    A segment belongs to the last chapter starting at or before it; segments
    before the first chapter's start join the first chapter.
    """
    ordered = sorted(chapters, key=lambda c: c.start)
    buckets = [[] for _ in ordered]
    index = 0
    for seg in segments:
        while index + 1 < len(ordered) and seg.start >= ordered[index + 1].start:
            index += 1
        buckets[index].append(seg)
    return [(c.title, b) for c, b in zip(ordered, buckets)]


def render_twin(metadata, transcript):
    """Render the twin body (no front-matter) as Markdown."""
    longest = max(
        [metadata.duration or 0] + [s.start for s in transcript.segments]
    )
    long_form = longest >= 3600
    kind = "auto-generated" if transcript.is_generated else "authored"

    lines = [f"# {metadata.title or 'Untitled YouTube video'}", ""]
    lines.append(f"- Channel: {metadata.channel or '(unknown)'}")
    lines.append(f"- Published: {metadata.upload_date or '(unknown)'}")
    if metadata.duration:
        lines.append(f"- Duration: {format_timestamp(metadata.duration, True)}")
    else:
        lines.append("- Duration: (unknown)")
    lines.append(
        f"- Transcript: {transcript.language} ({transcript.language_code}), {kind}"
    )
    lines += ["", "## Description", ""]
    lines.append(metadata.description or "(no description)")
    lines += ["", "## Transcript", ""]

    if metadata.chapters:
        for title, segs in _by_chapter(transcript.segments, metadata.chapters):
            lines += [f"### {title or 'Untitled chapter'}", ""]
            for paragraph in _paragraphs(segs, long_form):
                lines += [paragraph, ""]
    else:
        for paragraph in _paragraphs(transcript.segments, long_form):
            lines += [paragraph, ""]

    return "\n".join(lines).rstrip() + "\n"


def convert_youtube(source):
    """Convert a YouTube URL. Returns (markdown, canonical_source)."""
    vid = video_id(source)
    if vid is None:
        raise ConversionError(
            f"YouTube URL does not identify a single video (playlist, channel, "
            f"search, or home page): {source}; nothing captured"
        )
    metadata = fetch_metadata(vid)
    if metadata.live_status in ("is_live", "is_upcoming", "post_live"):
        raise ConversionError(
            f"YouTube video {vid} is still live or upcoming "
            f"({metadata.live_status}); capture it after it ends; nothing captured"
        )
    transcript = fetch_transcript(vid, metadata.language)
    return render_twin(metadata, transcript), canonical_url(vid)
