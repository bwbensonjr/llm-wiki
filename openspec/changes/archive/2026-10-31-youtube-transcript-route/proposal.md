## Why

Recorded conference talks, lectures, and interviews are a large share of what is
worth filing, and most of them live on YouTube. Today a YouTube URL is served as
`text/html`, so the router sends it to Jina Reader like any other web page. The
capture appears to work, but the twin holds the page chrome and the video
description, never what is said in the video. A summary authored from that twin is
a summary of the description. Nothing flags the gap on the unattended path, because
the description is usually long enough to pass the implausible-capture check.

The spoken content is available as captions: manual captions for many talks, and
auto-generated ones for most other videos. Capture should read the transcript, and
fail clearly when there is none, so the wiki never quietly files a thin twin.

## What Changes

- **Add a YouTube route** to the converter router. A source is recognized as a
  YouTube video by its **host and URL shape**, before content-type detection, because
  the served content type (`text/html`) cannot tell a video from an article.
  Recognized forms: `youtube.com/watch?v=`, `youtu.be/<id>`, `youtube.com/shorts/<id>`,
  `youtube.com/embed/<id>`, `youtube.com/live/<id>`, and the `m.` and `music.`
  subdomains.
- **Produce a transcript twin.** The twin contains the video's title (as H1),
  channel, publication date, duration, the transcript's language and whether it
  was authored or auto-generated, the description, and the full transcript. The
  transcript is grouped into timestamped paragraphs and divided by the video's
  chapters when it has any.
- **Record the route as `converter: youtube`** in the twin's front-matter.
- **Canonicalize the source URL.** The twin's `source:` records
  `https://www.youtube.com/watch?v=<id>`, dropping tracking (`si=`), timestamp
  (`t=`), and playlist (`list=`) parameters, so one video has one source no matter
  which share link was queued.
- **All-or-nothing on the transcript.** A video with no usable transcript, or one
  that is private, removed, members-only, age-gated, or live and not yet ended,
  fails capture with a reason that says which. No description-only twin is ever
  written. On the unattended path that entry is parked as `- [!]` like any other
  capture failure.
- **Detect duplicates by video ID.** The unattended duplicate check treats two
  YouTube URLs that name the same video as the same source.
- **Out of scope:** playlists and channel pages (a URL without a video ID fails
  capture, and says so), translating a transcript into another language, speech-to-text
  for videos with no captions, and other video hosts (Vimeo and similar).

## Capabilities

### New Capabilities

None. As with the PostScript route, this extends the existing converter router
rather than introducing a capability for one source kind.

### Modified Capabilities

- `resource-ingestion`: the **Content-type converter router** requirement gains the
  YouTube route and the rule that host recognition comes before content type. New
  requirements cover transcript twin contents, source canonicalization, and the
  no-transcript failure.
- `unattended-ingestion`: the **Duplicate sources are skipped** requirement compares
  YouTube sources by video ID rather than by literal URL string.

## Impact

- **Code**: `wiki_ingest/detect.py` (a `YOUTUBE` route, recognized by host and URL
  shape, checked before the content-type probe) and a new `wiki_ingest/youtube.py`
  (video-ID extraction, metadata and transcript fetching, twin rendering).
  `convert.capture()` records the canonical URL in `source:` for this route. Image
  localization is unaffected, since it runs only on the Jina route.
- **Dependencies**: two new Python packages, `youtube-transcript-api` (captions) and
  `yt-dlp` (metadata), both added with `uv add`. Neither needs an API key. Both talk
  to unofficial YouTube endpoints, so they break when YouTube changes and need
  version bumps from time to time (see design).
- **Tests**: routing for each URL form, canonicalization, transcript rendering,
  and every failure reason, using fakes with no network access.
- **Docs and skills**: the *Converter routing (Phase 1)* section of `CLAUDE.md`,
  plus the routing prose in `.claude/skills/file/SKILL.md` and
  `.claude/skills/ingest-inbox/SKILL.md` (which also gets the video-ID duplicate
  check). README gets a short note.
- **Corpus**: no existing `raw/` twin or `wiki/` page changes. A YouTube source
  already captured through Jina stays as it is; re-capturing it is the curator's
  decision.
