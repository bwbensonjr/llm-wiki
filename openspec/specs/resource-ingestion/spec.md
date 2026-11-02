# resource-ingestion Specification

## Purpose
TBD - created by archiving change add-resource-ingestion. Update Purpose after archive.
## Requirements
### Requirement: Knowledge page classification

The wiki SHALL classify every knowledge page with a `type` front-matter field
whose value is one of `summary`, `entity`, `concept`, or `analysis`. Knowledge
pages SHALL be stored under `wiki/` in a folder matching their type
(`wiki/summaries/`, `wiki/entities/`, `wiki/concepts/`, `wiki/analyses/`). The
wiki SHALL also maintain two bookkeeping files: `index.md` (a catalog) and
`log.md` (an append-only timeline).

#### Scenario: Summary page is source-anchored

- **WHEN** a source is ingested
- **THEN** exactly one page of type `summary` is created for it under
  `wiki/summaries/`

#### Scenario: Hub pages aggregate across sources

- **WHEN** a new summary references an entity or concept that already has a page
- **THEN** the existing `entity` or `concept` hub page is updated rather than
  duplicated

#### Scenario: Invalid type is rejected

- **WHEN** a page would be written with a `type` outside the defined set
- **THEN** the ingest is halted and the discrepancy is reported to the user
  rather than writing the page

### Requirement: Pages carry no review status

Knowledge pages SHALL NOT carry a `status` front-matter field. A page committed
by either ingest path, interactive or unattended, is final as committed; later
changes are ordinary edits.

#### Scenario: Interactive page has no status

- **WHEN** a page is committed through the interactive Phase 2 interview
- **THEN** its front-matter contains no `status` field

#### Scenario: Unattended page has no status

- **WHEN** a page is committed by the unattended ingest path
- **THEN** its front-matter contains no `status` field

### Requirement: Two-layer storage with immutable raw twin

The wiki SHALL store ingested content in two layers: an immutable `raw/` layer
holding a Markdown "twin" of each source, and an authored `wiki/` layer holding
LLM- and human-authored pages. A `raw/` twin once written SHALL NOT be edited by
later operations. Each `summary` page SHALL link to both its original source
(`source:`) and its raw twin (`raw:`) via front-matter.

#### Scenario: Raw twin is written immutably

- **WHEN** a source is converted during ingest
- **THEN** its Markdown twin is written to `raw/<date>-<slug>.md` and is not
  modified by any subsequent authoring step

#### Scenario: Summary links both ways

- **WHEN** a summary page is authored for an ingested source
- **THEN** its front-matter contains a `source:` pointing to the original
  URL/path and a `raw:` pointing to the local twin

### Requirement: Content-type converter router

The `file` command SHALL detect the content type of the resource and route
conversion accordingly: **YouTube video URLs to the YouTube transcript route**, web
URLs to Jina Reader, PDFs to Docling, **PostScript to ghostscript-then-Docling**, and
all other file types to MarkItDown. Detection SHALL consider the fetched content type,
not the file extension alone, so that a URL resolving to a PDF is routed to Docling.

A YouTube URL SHALL be recognized by its **host and URL shape**, and that check SHALL
come before content-type detection, because a YouTube video is served as `text/html`
and its content type cannot distinguish it from an ordinary web page. The recognized
hosts are `youtube.com`, `www.youtube.com`, `m.youtube.com`, `music.youtube.com`, and
`youtu.be`.

A source SHALL be recognized as PostScript when its fetched content type is
`application/postscript`, or when its path carries a PostScript extension (`.ps`,
`.eps`). A **gzipped** PostScript source SHALL also be recognized, by its `.ps.gz` path
even though the trailing extension is `.gz` and even though its served content type
(commonly `application/x-gzip`) does not identify the payload; it SHALL be decompressed
before conversion.

PostScript conversion is **two-stage**: ghostscript renders the source to PDF and the
existing Docling route converts that PDF to Markdown. The raw twin's `converter:` field
SHALL record that both stages ran rather than naming Docling alone, so the twin does not
misreport how it was produced.

Because ghostscript is an external system binary rather than a Python dependency, its
absence SHALL produce a failure that names the missing binary, distinguishable from a
source the converter could not parse.

A PostScript source built on **bitmap fonts** yields a PDF with no recoverable text
encoding, from which extraction produces unresolved glyph codes (`/65/98/115`) rather
than characters. Because such output parses as Markdown yet carries no readable prose,
and because `raw/` is immutable, capture SHALL refuse it rather than write it: when the
converted text is dominated by glyph-code tokens, conversion fails with a reason that
says the source has no recoverable text layer. Prose that merely carries **ligature
artifacts** — an `fl` rendered as `/`, so "flow" reads as "/ow" — SHALL NOT be refused,
because it remains legible.

#### Scenario: YouTube URL routes to the YouTube transcript route

- **WHEN** the user files a URL on a recognized YouTube host whose shape names a
  video, such as `https://www.youtube.com/watch?v=<id>` or `https://youtu.be/<id>`
- **THEN** the resource is converted by the YouTube transcript route, not Jina
  Reader, even though the URL is served as `text/html`, and the twin records
  `converter: youtube`

#### Scenario: Web URL routes to Jina Reader

- **WHEN** the user files an `http(s)` URL that resolves to an HTML page and is not
  a recognized YouTube URL
- **THEN** the resource is converted with Jina Reader

#### Scenario: PDF routes to Docling

- **WHEN** the user files a PDF, whether a local path or a URL resolving to PDF
  content
- **THEN** the resource is converted with Docling

#### Scenario: PostScript routes to ghostscript then Docling

- **WHEN** the user files a PostScript source, whether a local `.ps` path or a URL
  served as `application/postscript`
- **THEN** ghostscript converts it to PDF, Docling converts that PDF to Markdown, and
  the twin records the two-stage route

#### Scenario: Gzipped PostScript is recognized and decompressed

- **WHEN** the user files a `.ps.gz` source, whose trailing extension is `.gz` and whose
  served content type does not identify the payload
- **THEN** it is recognized as PostScript, decompressed, and converted by the same
  two-stage route

#### Scenario: Missing ghostscript is reported as such

- **WHEN** a PostScript source is filed on a machine where the ghostscript binary is not
  on `PATH`
- **THEN** conversion fails naming the missing binary, no twin is written, and the
  failure is distinguishable from unparseable content

#### Scenario: Unrecoverable glyph-code output is refused

- **WHEN** a PostScript source's fonts are bitmap fonts, so the converted text is
  dominated by unresolved glyph codes such as `/65/98/115` instead of characters
- **THEN** conversion fails saying the source has no recoverable text layer, and no twin
  is written

#### Scenario: Ligature artifacts are not refused

- **WHEN** a PostScript source converts to legible prose that carries ligature artifacts,
  such as `fl` rendered as `/` so that "flow analysis" reads as "/ow analysis"
- **THEN** the conversion succeeds and the twin is written, because the text is readable

#### Scenario: Other file types route to MarkItDown

- **WHEN** the user files a non-PDF, non-PostScript document such as `.docx`, `.pptx`,
  `.xlsx`, or an image
- **THEN** the resource is converted with MarkItDown

### Requirement: YouTube URL forms resolve to a single video ID

The YouTube route SHALL extract an 11-character video ID from every recognized URL
form: `watch?v=<id>`, `youtu.be/<id>`, `shorts/<id>`, `embed/<id>`, and `live/<id>`.
Query parameters other than the video ID, such as `si=`, `t=`, `list=`, and `index=`,
SHALL NOT affect which video is captured.

#### Scenario: Share link with tracking parameter

- **WHEN** the user files `https://youtu.be/<id>?si=<token>`
- **THEN** the video `<id>` is captured and the `si` parameter is ignored

#### Scenario: Watch URL inside a playlist

- **WHEN** the user files `https://www.youtube.com/watch?v=<id>&list=<playlist>&index=3`
- **THEN** only the video `<id>` is captured, not the playlist

#### Scenario: Shorts, embed, and live forms

- **WHEN** the user files a `youtube.com/shorts/<id>`, `youtube.com/embed/<id>`, or
  `youtube.com/live/<id>` URL, on the `www.`, `m.`, or `music.` host or no subdomain
- **THEN** the video `<id>` is captured by the YouTube route

### Requirement: YouTube URLs without a video are refused

A URL on a recognized YouTube host that names no single video, such as a playlist,
channel, search, or home page, SHALL fail capture with a reason saying the URL does
not identify a video. It SHALL NOT fall back to Jina Reader.

#### Scenario: Playlist URL is refused

- **WHEN** the user files `https://www.youtube.com/playlist?list=<playlist>`
- **THEN** capture fails saying the URL is not a single video, and no twin is written

#### Scenario: Channel URL is refused

- **WHEN** the user files `https://www.youtube.com/@<handle>`
- **THEN** capture fails saying the URL is not a single video, and no twin is written

### Requirement: YouTube twin records the canonical video URL

The raw twin of a YouTube source SHALL record `source: https://www.youtube.com/watch?v=<id>`
whatever form of URL was filed. A summary page authored from that twin SHALL carry the
same canonical URL in its `source:` field.

#### Scenario: Short link is canonicalized

- **WHEN** the user files `https://youtu.be/<id>?si=<token>&t=42`
- **THEN** the twin's front-matter contains `source: https://www.youtube.com/watch?v=<id>`

#### Scenario: Summary inherits the canonical URL

- **WHEN** a summary page is authored from a YouTube twin
- **THEN** the summary's `source:` equals the twin's canonical `source:`

### Requirement: YouTube twin contains metadata, description, and transcript

A YouTube twin's body SHALL open with the video title as its H1, then list the channel
name, publication date, duration, and the transcript's language and kind (authored or
auto-generated). It SHALL then contain the video description and the full transcript,
each under its own heading.

#### Scenario: Twin body carries metadata and transcript

- **WHEN** a video with a title, channel, description, and transcript is captured
- **THEN** the twin's H1 is the video title and its body carries the channel,
  publication date, duration, transcript language and kind, the description, and the
  full transcript

#### Scenario: Twin slug comes from the video title

- **WHEN** a YouTube video is captured
- **THEN** the twin is written to `raw/<date>-<slug>.md`, where the slug comes from the
  video title, not the video ID

#### Scenario: Empty description does not block capture

- **WHEN** a video with a usable transcript has an empty description
- **THEN** capture succeeds, and the twin says that the description is empty rather
  than leaving out the heading

### Requirement: YouTube transcript is timestamped and follows chapters

The transcript SHALL be rendered as paragraphs, each beginning with the timestamp of
its first caption in `[h:mm:ss]` or `[mm:ss]` form, so a later summary can cite a moment
in the video. When the video defines chapters, the transcript SHALL be divided under one
heading per chapter, named by the chapter title.

#### Scenario: Paragraphs carry timestamps

- **WHEN** a video's transcript is rendered
- **THEN** every transcript paragraph begins with a timestamp marking where in the video
  it starts

#### Scenario: Chapters become headings

- **WHEN** a video defines chapters
- **THEN** the transcript is split under one heading per chapter, in chapter order, and
  each paragraph sits under the chapter that contains its start time

#### Scenario: No chapters means one continuous transcript

- **WHEN** a video defines no chapters
- **THEN** the transcript is a single sequence of timestamped paragraphs under the
  transcript heading

### Requirement: YouTube transcript language selection

The YouTube route SHALL choose one transcript, preferring in order: authored English,
auto-generated English, authored in the video's original language, then auto-generated
in the video's original language. It SHALL NOT machine-translate a transcript. The
choice made SHALL be recorded in the twin's metadata.

#### Scenario: Authored captions preferred over auto-generated

- **WHEN** a video has both authored and auto-generated English captions
- **THEN** the authored captions are used and the twin records them as authored

#### Scenario: Auto-generated captions accepted

- **WHEN** a video's only English captions are auto-generated
- **THEN** capture succeeds using them and the twin records the transcript as
  auto-generated

#### Scenario: Non-English video keeps its own language

- **WHEN** a video has captions only in its original non-English language
- **THEN** the transcript is captured in that language, untranslated, and the twin
  records the language

### Requirement: YouTube capture without a transcript writes nothing

When no transcript can be obtained, the YouTube route SHALL fail capture and write no
twin. It SHALL NOT write a twin from metadata and description alone. The failure reason
SHALL name the cause: captions disabled or absent, video unavailable (private, removed,
members-only, or age-gated), live stream not yet ended, or YouTube refusing the request.

#### Scenario: Video with captions disabled

- **WHEN** the user files a video whose captions are disabled or absent
- **THEN** capture fails saying the video has no transcript, and no twin is written

#### Scenario: Unavailable video

- **WHEN** the user files a video that is private, removed, members-only, or age-gated
- **THEN** capture fails saying the video is unavailable, and no twin is written

#### Scenario: Live stream not yet ended

- **WHEN** the user files a live stream or premiere that has not finished
- **THEN** capture fails saying the video is still live, and no twin is written

#### Scenario: Request blocked by YouTube

- **WHEN** YouTube rejects the transcript request, for example by rate-limiting or
  blocking the requesting IP address
- **THEN** capture fails with a reason that says YouTube refused the request, so it is
  distinguishable from a video that has no transcript, and no twin is written

### Requirement: Two-phase file command

The `file` command SHALL operate in two phases. Phase 1 (capture) SHALL
mechanically convert the source and write the immutable `raw/` twin, performing
no wiki writes. Phase 2 (author) SHALL be an interactive interview in which the
LLM proposes a page type, tags, and `[[wikilinks]]`, the user reviews and
coaches, and only upon the user's commit does the LLM write the wiki pages.
Abandoning the command after Phase 1 SHALL leave only the raw twin and no wiki
changes.

#### Scenario: Phase 1 produces only the raw twin

- **WHEN** Phase 1 completes
- **THEN** the `raw/` twin exists and no files under `wiki/` have been created or
  modified

#### Scenario: Proposal is reviewed before commit

- **WHEN** the LLM presents its proposed type, tags, and links in Phase 2
- **THEN** the user can revise any of them, and the wiki pages are written only
  after the user commits

#### Scenario: Abandoning after Phase 1 is clean

- **WHEN** the user abandons the command during or before Phase 2
- **THEN** the only artifact left behind is the immutable `raw/` twin

### Requirement: Conversion failure writes nothing

The `file` command SHALL write no files when Phase 1 conversion fails, and SHALL
report the reason to the user. This applies to any failure cause, including an
unreachable source, content the converter cannot parse, or an unavailable
routed service. No `raw/` twin and no `wiki/` pages are left behind.

#### Scenario: Source cannot be converted

- **WHEN** the converter fails to produce Markdown for the source
- **THEN** no `raw/` twin or `wiki/` page is written, and the user is told why
  the conversion failed

### Requirement: Two-section summary pages

A `summary` page SHALL carry a `## Summary` section with the LLM's neutral
distillation of the source and a `## Why this matters` section with the
resource's significance to the curator. On the interactive path the curator
supplies the significance during the Phase 2 interview; on the unattended path
the LLM drafts it, seeded by the queue note when one was given. The body SHALL
NOT carry an inline authorship disclaimer.

#### Scenario: Both sections are present

- **WHEN** a summary page is committed by any path
- **THEN** it contains a `## Summary` section and a `## Why this matters` section,
  each non-empty

#### Scenario: Commentary is solicited on the interactive path

- **WHEN** the user has not yet provided commentary during an interactive Phase 2
  interview
- **THEN** the LLM prompts for the user's "why this matters" before committing the
  summary page

#### Scenario: Drafted commentary carries no disclaimer

- **WHEN** a summary's `## Why this matters` is drafted by the LLM on the
  unattended path
- **THEN** the page body contains no inline authorship disclaimer

### Requirement: Page prose is independent of corpus membership

A knowledge page's prose SHALL describe its subject, and SHALL NOT assert what the
wiki does or does not contain. The governing test is **falsifiability by ingest**: a
sentence is disallowed when ingesting some plausible future source would make it
false. This applies to every knowledge page type and to both authoring paths, and it
covers two classes of claim:

- **Presence or absence** — that a work is or is not an ingested source, that no page
  covers some topic, or that a page is the corpus's first on a subject.
- **Corpus-scoped superlatives and counts** — that something is the corpus's only,
  best, or earliest instance of a thing, or a count of how many pages mention it.

Where an absence would otherwise be stated, the page SHALL name what is true of the
subject and stop, rather than reporting what the corpus lacks.

Two things are explicitly **not** violations. **Sibling orientation** — situating a
subject among related pages, such as noting that an implementation sits alongside
other implementations the wiki covers — is permitted, because a later ingest adds to
such a grouping without falsifying it. **Superlatives scoped to a source** rather than
to the corpus are permitted, because their truth does not depend on corpus membership.

This constraint SHALL NOT apply to `wiki/log.md`, whose entries are dated,
append-only records of what was true when written.

A violation found after a page is written MAY be corrected by a curator edit. For a
`summary`, this SHALL be the one permitted exception to writing it once at ingest,
and it SHALL extend only to removing or rephrasing the offending claim, never to
revising the distillation.

#### Scenario: Absence claim is refused at authoring

- **WHEN** a page would state that some work is not an ingested source, or that no
  page in the wiki covers a topic
- **THEN** that claim is not written; the page names what is true of the subject
  instead

#### Scenario: Corpus-scoped superlative is refused at authoring

- **WHEN** a page would state that its subject is the corpus's only, first, or best
  instance of something, or would count the pages that mention it
- **THEN** that claim is not written

#### Scenario: Sibling orientation is permitted

- **WHEN** a hub page situates its subject among related pages the wiki already holds,
  without ranking them or asserting completeness
- **THEN** the prose is conformant and SHALL NOT be flagged or removed

#### Scenario: Source-scoped superlative is permitted

- **WHEN** a summary states a superlative about the source it summarizes, such as the
  only measurement that source reports
- **THEN** the prose is conformant, because a later ingest cannot falsify it

#### Scenario: Log entries are exempt

- **WHEN** a `wiki/log.md` entry records that no ingested source covered a topic at the
  time the entry was written
- **THEN** that entry is conformant and is never rewritten

#### Scenario: Stale claim in a summary is corrected narrowly

- **WHEN** the curator corrects a corpus-membership claim found in an existing
  `summary` page
- **THEN** only that claim is removed or rephrased and the surrounding distillation
  is left as written

### Requirement: Tag vocabulary preference at ingest

Both ingest paths SHALL prefer tags already in use over minting new ones. On the
interactive path a newly-minted tag SHALL be surfaced for the user to approve or
redirect before commit. On the unattended path a new tag MAY be committed, and
the run's `wiki/log.md` entry SHALL name every tag it minted. Corpus-wide
reconciliation of near-duplicate or orphan tags is left to `lint`.

#### Scenario: Existing tags are preferred

- **WHEN** the LLM proposes tags for a new page on either path
- **THEN** it draws from the tags already used in the wiki where they apply,
  rather than inventing near-duplicate tags

#### Scenario: New tags are surfaced for approval on the interactive path

- **WHEN** the LLM proposes a tag not already present in the wiki during an
  interactive interview
- **THEN** it flags the tag as new so the user can approve or redirect it before
  commit

#### Scenario: Unattended new tags are logged

- **WHEN** the unattended path commits a page carrying a tag not already present
  in the wiki
- **THEN** that ingest's `wiki/log.md` entry names the newly-minted tag

### Requirement: Bookkeeping updates on ingest

On each successful ingest the `file` command SHALL update `index.md` and
`log.md`. The `index.md` catalog SHALL list every wiki page with a link and a
one-line summary, grouped by type. The `log.md` file SHALL receive an appended,
greppable entry recording the ingest.

#### Scenario: Index gains the new page

- **WHEN** a new wiki page is committed
- **THEN** `index.md` is updated to include a link to that page with a one-line
  summary under its type grouping

#### Scenario: Log records the ingest

- **WHEN** an ingest completes
- **THEN** a new entry is appended to `log.md` recording what was ingested and
  when, without rewriting existing entries

### Requirement: Markdown and Obsidian compatibility

All wiki pages SHALL be Markdown with YAML front-matter and SHALL use
Obsidian-compatible `[[wikilinks]]` for cross-references between pages. Links
SHALL resolve by page filename independent of folder location.

#### Scenario: Cross-references use wikilinks

- **WHEN** a summary page references an entity or concept page
- **THEN** the reference is written as an Obsidian `[[wikilink]]` that resolves
  by filename
