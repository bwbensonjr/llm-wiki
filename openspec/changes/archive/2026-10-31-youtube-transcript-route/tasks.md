# Tasks

## 1. Dependencies

- [x] 1.1 Run `uv add youtube-transcript-api yt-dlp` and verify `uv run python -c "import youtube_transcript_api, yt_dlp"` succeeds and `uv.lock` is updated

## 2. URL recognition and canonicalization

- [x] 2.1 Add `wiki_ingest/youtube.py` with `video_id(url)` (returns the 11-character ID or `None`) and `canonical_url(video_id)`, covering `watch?v=`, `youtu.be/`, `shorts/`, `embed/`, `live/` on the bare, `www.`, `m.`, and `music.` hosts, and ignoring `si`, `t`, `list`, and `index`. Verify with parametrized tests in `tests/test_youtube.py`
- [x] 2.2 Add a `YOUTUBE = "youtube"` route to `wiki_ingest/detect.py`, checked by host before the content-type probe so that no network request is made. Verify with tests that a YouTube URL routes to `YOUTUBE` using a `FakeSession` that records zero requests, that a playlist or channel URL on a YouTube host also routes to `YOUTUBE`, and that a non-YouTube HTML URL still routes to `JINA`
- [x] 2.3 Add `wiki-capture --canonical <source>` to `wiki_ingest/cli.py`, which prints `{"source": ...}` and exits 0 without network access or writes. Verify with CLI tests for a `youtu.be` link with `si=` (canonicalized) and a non-YouTube URL (returned unchanged)

## 3. Metadata and transcript fetching

- [x] 3.1 In `youtube.py`, wrap yt-dlp `extract_info(download=False)` in a thin `fetch_metadata(video_id)` that returns title, channel, upload date, duration, description, chapters, `live_status`, `availability`, and language. Verify with a test that a faked yt-dlp payload is mapped into those fields
- [x] 3.2 Wrap `youtube-transcript-api` in `fetch_transcript(video_id, original_language)` that applies the spec's selection order (authored English, generated English, authored original, generated original) and never translates. Verify with tests over a faked transcript list for each branch of the order
- [x] 3.3 Map every failure to a standalone `ConversionError` naming the video ID and cause: no video ID in the URL, captions disabled or absent, unavailable (private, removed, members-only, age-gated), still live or upcoming, and request blocked. Check live status from metadata before any caption request. Verify with one test per cause, asserting the message text and that the blocked-request message differs from the no-transcript one

## 4. Twin rendering and capture integration

- [x] 4.1 Implement `render_twin(metadata, transcript)` following design decision 4: H1 title, metadata list, `## Description` (or `(no description)`), and `## Transcript` with optional `###` chapter headings. Verify with a snapshot-style test for a video with chapters and one without
- [x] 4.2 Implement paragraph grouping (about 60 seconds, forced break at chapter boundaries, `[mm:ss]` or `[h:mm:ss]` used consistently across the twin, whitespace normalized, HTML entities decoded, caption tokens such as `[Music]` kept). Verify with tests for a paragraph that crosses a chapter boundary, a video longer than an hour, and an entity-encoded segment
- [x] 4.3 Wire the `YOUTUBE` route into `convert.convert()`, add a `source` field to `CaptureResult`, and have `capture()` write that canonical source into the front-matter. Verify with a capture test (fakes for both libraries) that the twin has `source: https://www.youtube.com/watch?v=<id>`, `converter: youtube`, a slug from the video title, and no `raw/assets/` directory
- [x] 4.4 Add `"source"` to the CLI's JSON output on success. Verify with a CLI test that captures a faked `youtu.be` link and checks the canonical `source` in stdout
- [x] 4.5 Verify all-or-nothing: a capture test where the transcript fetch fails after metadata succeeded leaves `raw/` empty, and `uv run pytest` passes in full

## 5. Docs and skills

- [x] 5.1 Update the *Converter routing (Phase 1)* section of `CLAUDE.md`: add the YouTube route, the host-before-content-type rule, canonical `source:`, and the no-transcript failure, and update the twin `converter:` value list to `jina | docling | markitdown | ghostscript+docling | youtube`. Verify by reading the section against the spec
- [x] 5.2 Update `.claude/skills/file/SKILL.md` routing prose, and tell it to use the CLI's returned `source` for the summary's `source:`. Verify the routing list names all five routes
- [x] 5.3 Update `.claude/skills/ingest-inbox/SKILL.md`: add routing prose, use the returned `source` for the summary, and change step 2a to run `wiki-capture --canonical` on each entry before comparing it against existing `source:` values. Verify that step 2a's text describes the canonical comparison
- [x] 5.4 Add a README note on YouTube support, auto-generated caption quality, possible IP blocking from cloud hosts, and the `uv lock --upgrade-package yt-dlp youtube-transcript-api` fix for breakages. Verify that the note is present and that the command in it runs

## 6. End-to-end check

- [x] 6.1 From a local machine, run `uv run wiki-capture --raw-dir <scratch> <real youtu.be share link>` on a talk with authored captions and chapters, and on a talk with only auto-generated captions. Verify both twins match the design layout. Then run it on a video with captions disabled and verify that nothing is written and the reason names the cause
- [x] 6.2 Run `mise exec -- openspec validate youtube-transcript-route --strict` and verify it passes

## Workflow follow-up

- Archive the change with `/opsx:archive` once implemented and reviewed, which syncs the delta specs into `openspec/specs/resource-ingestion` and `openspec/specs/unattended-ingestion`.
