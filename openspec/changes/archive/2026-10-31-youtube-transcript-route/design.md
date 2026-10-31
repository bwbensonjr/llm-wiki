## Context

`detect.detect()` probes a URL's content type with a HEAD (falling back to a ranged
GET) and routes on the result. A YouTube watch page answers `text/html`, so it goes
to Jina. In some regions YouTube also answers the probe with a consent interstitial,
which says even less. `convert.capture()` writes `source: {source}` exactly as it was
given, and the skills copy that value into the summary's `source:`. The unattended
duplicate check (`ingest-inbox` step 2a) compares the queued string against existing
`source:` values.

See proposal.md for motivation and the specs for the required behavior.

## Goals / Non-Goals

**Goals:**

- Capture spoken content as text, with enough structure (timestamps, chapters) that a
  summary can refer to a moment in a long talk.
- Keep every failure mechanical and self-explanatory. The unattended path writes the
  error string straight into an `inbox.md` park annotation, and the curator sees
  nothing else.
- No API keys and no new system binaries.

**Non-Goals:**

- Speech-to-text (Whisper or similar) for videos with no captions. It is a heavy
  dependency and would produce a different kind of artifact. Revisit only if
  caption-less talks pile up as parked entries.
- Cookies, proxies, or other ways around YouTube's IP blocking.
- Localizing the thumbnail or any frames. Image localization stays Jina-only.
- Re-capturing YouTube sources that were already filed through Jina.

## Decisions

### 1. Recognize YouTube by host, before the content-type probe

`detect.detect()` checks the URL against the YouTube host set first and returns
`(YOUTUBE, "youtube")` without making a network request. URLs on a YouTube host that
name no video (playlists, channels, search) also take the YouTube route, and the route
refuses them with a clear reason. Otherwise they would fall through to Jina and
produce exactly the thin twin this change exists to prevent.

*Alternative:* probe first and special-case `text/html` from YouTube hosts. Rejected:
it spends a request to learn nothing, and the consent-interstitial response makes it
less reliable, not more.

### 2. `youtube-transcript-api` for captions, `yt-dlp` for metadata

- **Captions: `youtube-transcript-api`.** It returns clean `(text, start, duration)`
  segments and lists the available transcripts with language and an
  `is_generated` flag, which is exactly what the language-selection order needs. Its
  typed exceptions (`TranscriptsDisabled`, `NoTranscriptFound`, `VideoUnavailable`,
  `AgeRestricted`, `RequestBlocked`/`IpBlocked`) map one-to-one onto the failure
  reasons in the spec.
- **Metadata: `yt-dlp`**, called as a library with `extract_info(url, download=False)`.
  It returns title, channel, upload date, duration, full description, chapters,
  `live_status`, `availability`, and the video's original `language`. Nothing is
  downloaded.

*Alternatives considered:*

- **MarkItDown's built-in YouTube converter.** It is already a dependency, but it
  scrapes page `<meta>` tags, has no chapters, cannot tell authored captions from
  generated ones, and **silently omits the transcript when it cannot fetch one**.
  That last point breaks the all-or-nothing rule.
- **yt-dlp alone**, downloading caption files as VTT. One dependency instead of two,
  but auto-generated VTT repeats each line as it scrolls, so it would need a
  de-duplication pass that `youtube-transcript-api` makes unnecessary.
- **YouTube Data API v3.** It needs an API key, and downloading captions through it
  needs OAuth as the video's owner. Not usable for other people's videos.
- **oEmbed for metadata.** No key, but no description, duration, or chapters.

### 3. Fetch metadata first, then the transcript

Metadata comes first because it settles three things before any caption request:
whether the video is available (`availability`), whether it is still live
(`live_status` of `is_live` or `is_upcoming` fails fast), and which language is
"original" for the selection order. Then the transcript list is fetched and the first
match in the spec's order is taken. When yt-dlp reports no `language`, the original
language falls back to the language of the first listed authored transcript, then to
the first auto-generated one.

### 4. Twin layout

```markdown
---
source: https://www.youtube.com/watch?v=dQw4w9WgXcQ
fetched-at: 2026-10-31
converter: youtube
---

# <video title>

- Channel: <channel name>
- Published: <YYYY-MM-DD>
- Duration: <h:mm:ss>
- Transcript: <language name> (<code>), authored | auto-generated

## Description

<description verbatim, or "(no description)">

## Transcript

### <chapter title>

[00:00] <paragraph>

[01:04] <paragraph>
```

The front-matter keeps exactly the three twin fields. Transcript language and kind go
in the body, so the twin front-matter schema (and `lint`'s check of it) does not
change. Without chapters there are no `###` headings.

The description goes in verbatim, links included. `raw/` is a mechanical twin, and
deciding what in a description is noise is authoring judgment.

### 5. Paragraph grouping

Auto-generated captions have no sentence punctuation, so paragraphs are grouped by
time: consecutive segments join a paragraph until it spans about 60 seconds, then the
paragraph breaks at the next segment boundary. A chapter boundary always forces a
break. Segment text has its whitespace normalized and HTML entities decoded. Nothing
else changes, so caption tokens such as `[Music]` and `[Applause]` stay in. The
timestamp format is `[mm:ss]`, or `[h:mm:ss]` throughout when the video runs an hour
or more. The format is consistent within a twin.

*Alternative:* one line per caption segment. Rejected: a one-hour talk produces about
1,500 short lines. That is unreadable in Obsidian, and its density buys nothing for
summarizing.

### 6. `converter: youtube`, not the library names

The `converter:` value names the route. The PostScript precedent recorded two stages
because both stages produced the text in the twin. Here the decision that matters for
auditing is authored versus auto-generated captions, and the body records that.
Putting library names in an immutable field would tie every twin to an implementation
choice that is likely to change.

### 7. Canonical source flows out of capture

The YouTube route returns the canonical URL along with the Markdown. `CaptureResult`
gains a `source` field (the filed string unchanged for every other route), and
`capture()` writes that field into the front-matter. The CLI's JSON output adds
`"source"`, and both skills use that value, not the string they were given, for the
summary's `source:`.

### 8. A no-network canonicalization flag for duplicate checks

`ingest-inbox` checks for duplicates *before* capture, so it needs the canonical form
without fetching anything. `wiki-capture --canonical <source>` prints
`{"source": "<canonical>"}` and exits. It does no network work and writes nothing. For
a non-YouTube source it returns the input unchanged. Step 2a of the skill runs it on
each entry and compares the result against existing `source:` values. The comparison
stays a plain string match, and parsing video IDs stays in tested code rather than in
skill prose.

*Alternative:* let the skill pull out the video ID itself. Rejected: URL parsing done
by an LLM is exactly the kind of step that drifts across runs.

### 9. Error messages stand alone

Every failure becomes a `ConversionError` whose message names the video ID and the
cause in words the curator can act on, for example `YouTube video <id> has no
transcript (captions disabled); nothing captured`. A blocked request says so and
suggests retrying later from a different network, so it is not mistaken for a video
that permanently lacks captions.

## Risks / Trade-offs

- **Unofficial endpoints break.** Both libraries scrape interfaces YouTube does not
  promise to keep stable, and breakages arrive without notice. → Failures are clear
  and park the entry rather than corrupting anything, and the fix is usually
  `uv lock --upgrade-package yt-dlp youtube-transcript-api`. The README says so.
- **IP blocking from cloud hosts.** YouTube regularly blocks transcript requests from
  datacenter IPs, so a scheduled cloud run of `ingest-inbox` may park every YouTube
  entry while a laptop run succeeds. → A distinct "YouTube refused the request"
  reason keeps this diagnosable. Parked entries are not retried automatically, so the
  curator re-queues them after a local run.
- **Auto-generated transcript quality.** Mis-heard names and technical terms (an
  auto-caption can render "Chez Scheme" as "chase scheme") land in an immutable
  twin. → The same stance as ligature artifacts: tolerated, not repaired. The twin's
  metadata flags the transcript as auto-generated so the authoring step can treat
  proper nouns with suspicion.
- **Very long videos.** A three-hour podcast is roughly 30,000 words in one twin. →
  Accepted. It is still far smaller than many PDFs, and chapters plus timestamps keep
  it navigable.
- **Two dependencies where one might do.** → Accepted for the clean segment API and
  the typed errors (decision 2). yt-dlp is pure Python and installs with `uv`.

## Migration Plan

Additive. Install the dependencies with `uv add youtube-transcript-api yt-dlp`. No
existing twin, page, or front-matter changes. Rollback is reverting the commit: a
YouTube URL then goes back to the Jina route.
