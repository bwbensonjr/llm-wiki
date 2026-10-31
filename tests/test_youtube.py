"""YouTube route: URL parsing, routing, transcript selection, rendering, capture.

No test here touches the network. `_extract_info` (yt-dlp) and
`_list_transcripts` (youtube-transcript-api) are the only two calls that would,
and both are replaced with fakes.
"""

import json

import pytest
import youtube_transcript_api as yta
from yt_dlp.utils import DownloadError

from wiki_ingest import cli, convert, detect, youtube
from wiki_ingest.convert import ConversionError

VID = "dQw4w9WgXcQ"
CANON = f"https://www.youtube.com/watch?v={VID}"


# --- URL parsing and canonicalization ----------------------------------------


@pytest.mark.parametrize(
    "url",
    [
        f"https://www.youtube.com/watch?v={VID}",
        f"https://youtube.com/watch?v={VID}",
        f"https://m.youtube.com/watch?v={VID}",
        f"https://music.youtube.com/watch?v={VID}",
        f"https://youtu.be/{VID}",
        f"https://youtu.be/{VID}?si=AbCdEfGh123",
        f"https://youtu.be/{VID}?si=AbCdEfGh123&t=42",
        f"https://www.youtube.com/watch?v={VID}&list=PLxyz&index=3",
        f"https://www.youtube.com/watch?t=90&v={VID}",
        f"https://www.youtube.com/shorts/{VID}",
        f"https://m.youtube.com/shorts/{VID}?feature=share",
        f"https://www.youtube.com/embed/{VID}",
        f"https://www.youtube.com/live/{VID}?si=x",
        f"http://youtube.com/embed/{VID}",
    ],
)
def test_video_id_from_every_form(url):
    assert youtube.video_id(url) == VID
    assert youtube.canonical_source(url) == CANON


@pytest.mark.parametrize(
    "url",
    [
        "https://www.youtube.com/playlist?list=PLxyz",
        "https://www.youtube.com/@somechannel",
        "https://www.youtube.com/results?search_query=scheme",
        "https://www.youtube.com/",
        "https://www.youtube.com/watch?v=tooshort",
        "https://youtu.be/",
    ],
)
def test_url_without_a_video_has_no_id(url):
    assert youtube.video_id(url) is None
    assert youtube.canonical_source(url) == url


def test_non_youtube_source_is_unchanged():
    for source in ["https://example.com/watch?v=dQw4w9WgXcQ", "inbox-files/a.pdf"]:
        assert youtube.canonical_source(source) == source


# --- routing -----------------------------------------------------------------


class NoNetworkSession:
    """Fails the test if detection makes any request."""

    def head(self, *a, **k):
        raise AssertionError("YouTube detection must not probe the network")

    get = head


@pytest.mark.parametrize(
    "url",
    [
        f"https://youtu.be/{VID}?si=x",
        f"https://www.youtube.com/watch?v={VID}",
        "https://www.youtube.com/playlist?list=PLxyz",
        "https://www.youtube.com/@somechannel",
    ],
)
def test_youtube_urls_route_without_a_probe(url):
    route, detected = detect.detect(url, session=NoNetworkSession())
    assert route == detect.YOUTUBE
    assert detected == "youtube"


def test_ordinary_html_still_routes_to_jina():
    from .conftest import FakeSession

    route, _ = detect.detect("https://example.com/post", session=FakeSession())
    assert route == detect.JINA


# --- CLI --canonical ---------------------------------------------------------


def run_cli(capsys, argv):
    code = cli.main(argv)
    out = capsys.readouterr()
    return code, out


def test_cli_canonical_youtube(capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    code, out = run_cli(capsys, ["--canonical", f"https://youtu.be/{VID}?si=abc"])
    assert code == 0
    assert json.loads(out.out) == {"source": CANON}
    assert list(tmp_path.iterdir()) == []


def test_cli_canonical_passthrough(capsys):
    code, out = run_cli(capsys, ["--canonical", "https://example.com/a?b=c"])
    assert code == 0
    assert json.loads(out.out) == {"source": "https://example.com/a?b=c"}


# --- fakes for the two libraries ---------------------------------------------


class FakeTranscript:
    def __init__(self, code, generated, segments=None, language=None, error=None):
        self.language_code = code
        self.is_generated = generated
        self.language = language or {"en": "English", "fr": "French"}.get(
            code.split("-")[0], code
        )
        self._segments = segments if segments is not None else [("hello", 0.0)]
        self._error = error

    def fetch(self):
        if self._error:
            raise self._error
        return [
            yta.FetchedTranscriptSnippet(text=t, start=s, duration=1.0)
            for t, s in self._segments
        ]


def info(**overrides):
    base = {
        "title": "Compilers in Sixty Minutes",
        "channel": "PL Talks",
        "upload_date": "20240305",
        "duration": 1830,
        "description": "A talk about compilers.\nhttps://example.com/slides",
        "chapters": None,
        "language": "en",
        "live_status": "not_live",
        "availability": "public",
    }
    base.update(overrides)
    return base


@pytest.fixture
def fake_youtube(monkeypatch):
    """Install fakes; returns a dict the test fills with `info` and `listing`."""
    state = {"info": info(), "listing": [FakeTranscript("en", False)], "calls": []}

    def extract(url):
        state["calls"].append("metadata")
        if isinstance(state["info"], Exception):
            raise state["info"]
        return state["info"]

    def listing(vid):
        state["calls"].append("transcripts")
        if isinstance(state["listing"], Exception):
            raise state["listing"]
        return state["listing"]

    monkeypatch.setattr(youtube, "_extract_info", extract)
    monkeypatch.setattr(youtube, "_list_transcripts", listing)
    return state


# --- metadata ----------------------------------------------------------------


def test_generated_language_name_drops_kind_suffix(fake_youtube):
    fake_youtube["listing"] = [
        FakeTranscript("en", True, language="English (auto-generated)")
    ]
    t = youtube.fetch_transcript(VID, "en")
    assert t.language == "English"
    assert t.is_generated


def test_fetch_metadata_maps_fields(fake_youtube):
    fake_youtube["info"] = info(
        chapters=[{"title": "Intro", "start_time": 0.0}, {"title": "Parsing", "start_time": 120.0}]
    )
    m = youtube.fetch_metadata(VID)
    assert m.title == "Compilers in Sixty Minutes"
    assert m.channel == "PL Talks"
    assert m.upload_date == "2024-03-05"
    assert m.duration == 1830
    assert m.description.startswith("A talk about compilers.")
    assert [(c.title, c.start) for c in m.chapters] == [("Intro", 0.0), ("Parsing", 120.0)]
    assert m.language == "en"


def test_channel_falls_back_to_uploader(fake_youtube):
    fake_youtube["info"] = info(channel=None, uploader="someone")
    assert youtube.fetch_metadata(VID).channel == "someone"


# --- transcript selection ----------------------------------------------------


def pick(listing, original):
    chosen = youtube.select_transcript(listing, original)
    return None if chosen is None else (chosen.language_code, chosen.is_generated)


def test_authored_english_beats_generated_english():
    listing = [FakeTranscript("en", True), FakeTranscript("en", False)]
    assert pick(listing, "en") == ("en", False)


def test_generated_english_beats_authored_original():
    listing = [FakeTranscript("fr", False), FakeTranscript("en", True)]
    assert pick(listing, "fr") == ("en", True)


def test_regional_english_counts_as_english():
    assert pick([FakeTranscript("en-GB", False)], "en") == ("en-GB", False)


def test_authored_original_beats_generated_original():
    listing = [FakeTranscript("fr", True), FakeTranscript("fr", False)]
    assert pick(listing, "fr") == ("fr", False)


def test_generated_original_is_last_resort():
    assert pick([FakeTranscript("fr", True)], "fr") == ("fr", True)


def test_unknown_original_falls_back_to_first_authored():
    listing = [FakeTranscript("de", True), FakeTranscript("fr", False)]
    assert pick(listing, None) == ("fr", False)


def test_no_translation_to_an_unrelated_language():
    assert pick([FakeTranscript("de", False)], "fr") is None


# --- failure reasons ---------------------------------------------------------


def test_no_video_id_is_refused():
    with pytest.raises(ConversionError, match="does not identify a single video"):
        youtube.convert_youtube("https://www.youtube.com/playlist?list=PLxyz")


@pytest.mark.parametrize("status", ["is_live", "is_upcoming"])
def test_live_is_refused_before_any_caption_request(fake_youtube, status):
    fake_youtube["info"] = info(live_status=status)
    with pytest.raises(ConversionError, match="still live or upcoming"):
        youtube.convert_youtube(CANON)
    assert fake_youtube["calls"] == ["metadata"]


def test_upcoming_reported_by_ytdlp_is_live(fake_youtube):
    fake_youtube["info"] = DownloadError("ERROR: This live event will begin in 3 hours.")
    with pytest.raises(ConversionError, match="still live or upcoming"):
        youtube.convert_youtube(CANON)


@pytest.mark.parametrize(
    "message, why",
    [
        ("ERROR: [youtube] x: Private video. Sign in", "private"),
        ("ERROR: Join this channel to get access to members-only content", "members-only"),
        ("ERROR: Sign in to confirm your age", "age-gated"),
        ("ERROR: Video unavailable. This video has been removed", "removed"),
    ],
)
def test_unavailable_reasons_from_ytdlp(fake_youtube, message, why):
    fake_youtube["info"] = DownloadError(message)
    with pytest.raises(ConversionError, match=f"unavailable \\({why}"):
        youtube.convert_youtube(CANON)


def test_ytdlp_bot_check_is_reported_as_blocked(fake_youtube):
    fake_youtube["info"] = DownloadError("ERROR: Sign in to confirm you're not a bot")
    with pytest.raises(ConversionError, match="YouTube refused the request"):
        youtube.convert_youtube(CANON)


def test_captions_disabled(fake_youtube):
    fake_youtube["listing"] = yta.TranscriptsDisabled(VID)
    with pytest.raises(ConversionError, match="has no transcript \\(captions disabled"):
        youtube.convert_youtube(CANON)


def test_no_matching_language(fake_youtube):
    fake_youtube["info"] = info(language="fr")
    fake_youtube["listing"] = [FakeTranscript("de", False)]
    with pytest.raises(ConversionError, match="has no transcript"):
        youtube.convert_youtube(CANON)


@pytest.mark.parametrize("exc_type", [yta.RequestBlocked, yta.IpBlocked])
def test_blocked_differs_from_missing_transcript(fake_youtube, exc_type):
    fake_youtube["listing"] = exc_type(VID)
    with pytest.raises(ConversionError) as caught:
        youtube.convert_youtube(CANON)
    message = str(caught.value)
    assert "YouTube refused the request" in message
    assert "not a missing transcript" in message
    assert "has no transcript" not in message


def test_blocked_on_fetch_is_also_blocked(fake_youtube):
    fake_youtube["listing"] = [FakeTranscript("en", False, error=yta.RequestBlocked(VID))]
    with pytest.raises(ConversionError, match="YouTube refused the request"):
        youtube.convert_youtube(CANON)


def test_unavailable_from_transcript_api(fake_youtube):
    fake_youtube["listing"] = yta.VideoUnavailable(VID)
    with pytest.raises(ConversionError, match="is unavailable"):
        youtube.convert_youtube(CANON)


def test_failure_messages_name_the_video(fake_youtube):
    fake_youtube["listing"] = yta.TranscriptsDisabled(VID)
    with pytest.raises(ConversionError, match=VID):
        youtube.convert_youtube(CANON)


# --- rendering ---------------------------------------------------------------


def transcript(segments, generated=False, code="en"):
    return youtube.Transcript(
        language="English",
        language_code=code,
        is_generated=generated,
        segments=[youtube.Segment(text=t, start=s) for t, s in segments],
    )


def metadata(**overrides):
    base: dict = dict(
        title="Compilers in Sixty Minutes",
        channel="PL Talks",
        upload_date="2024-03-05",
        duration=1830,
        description="A talk about compilers.",
        chapters=[],
        language="en",
    )
    base.update(overrides)
    return youtube.Metadata(**base)  # type: ignore[arg-type]


def test_render_without_chapters():
    body = youtube.render_twin(
        metadata(),
        transcript([("so today", 0.0), ("we talk", 2.5), ("about parsing", 61.0)], generated=True),
    )
    assert body == (
        "# Compilers in Sixty Minutes\n"
        "\n"
        "- Channel: PL Talks\n"
        "- Published: 2024-03-05\n"
        "- Duration: 0:30:30\n"
        "- Transcript: English (en), auto-generated\n"
        "\n"
        "## Description\n"
        "\n"
        "A talk about compilers.\n"
        "\n"
        "## Transcript\n"
        "\n"
        "[00:00] so today we talk\n"
        "\n"
        "[01:01] about parsing\n"
    )
    assert "###" not in body


def test_render_with_chapters_breaks_at_boundary():
    chapters = [youtube.Chapter("Intro", 0.0), youtube.Chapter("Parsing", 20.0)]
    body = youtube.render_twin(
        metadata(chapters=chapters),
        transcript([("hello", 0.0), ("welcome", 10.0), ("tokens first", 21.0), ("then trees", 30.0)]),
    )
    intro, parsing = body.split("### Intro\n")[1].split("### Parsing\n")
    assert "[00:00] hello welcome" in intro
    assert "tokens" not in intro
    assert "[00:21] tokens first then trees" in parsing
    assert "- Transcript: English (en), authored" in body


def test_segments_before_first_chapter_join_it():
    chapters = [youtube.Chapter("Main", 5.0)]
    body = youtube.render_twin(
        metadata(chapters=chapters), transcript([("early", 1.0), ("later", 6.0)])
    )
    assert "### Main\n\n[00:01] early later" in body


def test_long_video_uses_hour_timestamps_throughout():
    body = youtube.render_twin(
        metadata(duration=4000),
        transcript([("start", 0.0), ("much later", 3700.0)]),
    )
    assert "[0:00:00] start" in body
    assert "[1:01:40] much later" in body


def test_entities_decoded_whitespace_normalized_tokens_kept():
    body = youtube.render_twin(
        metadata(),
        transcript([("[Music]", 0.0), ("Tom &amp; Jerry\n  say &#39;hi&#39;", 1.0)]),
    )
    assert "[00:00] [Music] Tom & Jerry say 'hi'" in body


def test_empty_description_is_stated():
    body = youtube.render_twin(metadata(description=""), transcript([("x", 0.0)]))
    assert "## Description\n\n(no description)\n" in body


# --- capture integration -----------------------------------------------------


def test_capture_writes_canonical_twin(fake_youtube, tmp_path):
    raw = tmp_path / "raw"
    result = convert.capture(
        f"https://youtu.be/{VID}?si=abc&t=42",
        raw_dir=raw,
        session=NoNetworkSession(),
    )
    text = result.raw_path.read_text()
    assert text.startswith(
        f"---\nsource: {CANON}\nfetched-at: "
    )
    assert "converter: youtube\n" in text
    assert result.source == CANON
    assert result.converter == "youtube"
    assert result.raw_path.name.endswith("-compilers-in-sixty-minutes.md")
    assert result.title == "Compilers in Sixty Minutes"
    assert result.images is None
    assert not (raw / "assets").exists()


def test_transcript_failure_after_metadata_writes_nothing(fake_youtube, tmp_path):
    raw = tmp_path / "raw"
    fake_youtube["listing"] = yta.TranscriptsDisabled(VID)
    with pytest.raises(ConversionError):
        convert.capture(CANON, raw_dir=raw, session=NoNetworkSession())
    assert fake_youtube["calls"] == ["metadata", "transcripts"]
    assert not raw.exists() or list(raw.iterdir()) == []


def test_cli_reports_canonical_source(fake_youtube, tmp_path, capsys):
    code, out = run_cli(
        capsys, ["--raw-dir", str(tmp_path / "raw"), f"https://youtu.be/{VID}?si=abc"]
    )
    assert code == 0
    payload = json.loads(out.out)
    assert payload["source"] == CANON
    assert payload["converter"] == "youtube"


def test_cli_reports_failure_reason(fake_youtube, tmp_path, capsys):
    fake_youtube["listing"] = yta.TranscriptsDisabled(VID)
    code, out = run_cli(capsys, ["--raw-dir", str(tmp_path / "raw"), CANON])
    assert code == 1
    assert "captions disabled" in json.loads(out.err)["error"]
