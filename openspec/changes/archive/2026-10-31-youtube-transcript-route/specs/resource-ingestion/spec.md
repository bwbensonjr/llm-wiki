## MODIFIED Requirements

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

## ADDED Requirements

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
