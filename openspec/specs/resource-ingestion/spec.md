# resource-ingestion Specification

## Purpose
TBD - created by archiving change add-resource-ingestion. Update Purpose after archive.
## Requirements
### Requirement: Wiki page taxonomy

The wiki SHALL classify every knowledge page with a `type` front-matter field
whose value is one of `summary`, `entity`, `concept`, or `analysis`, following
Karpathy's content-oriented classification. Every knowledge page SHALL additionally
carry a `status` front-matter field whose value is one of `provisional` (authored
without curator review) or `reviewed` (curator-endorsed). The wiki SHALL
additionally maintain two bookkeeping files: `index.md` (a catalog) and `log.md`
(an append-only timeline). Knowledge pages SHALL be stored under `wiki/` in a
folder matching their type (`wiki/summaries/`, `wiki/entities/`, `wiki/concepts/`,
`wiki/analyses/`).

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

#### Scenario: Interactive ingest writes reviewed pages

- **WHEN** a page is committed through the interactive Phase 2 interview
- **THEN** it carries `status: reviewed`, because the curator approved it as it was
  written

#### Scenario: Invalid status is rejected

- **WHEN** a page would be written with a `status` outside `provisional|reviewed`
- **THEN** the ingest is halted and the discrepancy is reported rather than writing
  the page

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
conversion accordingly: web URLs to Jina Reader, PDFs to Docling, **PostScript to
ghostscript-then-Docling**, and all other file types to MarkItDown. Detection SHALL
consider the fetched content type, not the file extension alone, so that a URL
resolving to a PDF is routed to Docling.

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

#### Scenario: Web URL routes to Jina Reader

- **WHEN** the user files an `http(s)` URL that resolves to an HTML page
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

### Requirement: Dual-voice summary pages

A `summary` page SHALL carry two distinct sections: a `## Summary` section
containing the LLM's neutral distillation of the source, and a `## Why this
matters` section containing the significance of the resource to the curator. The
`## Why this matters` section is **endorsement-gated rather than
authorship-gated**: it MAY be drafted by the LLM while the page carries
`status: provisional`, and it becomes curator-endorsed when the page is moved to
`status: reviewed`. On the interactive path the curator supplies this commentary in
their own words during the Phase 2 interview and the page is `reviewed` on commit.
On the unattended path the LLM drafts it — seeded by the curator's queue note where
one was given — and the page is `provisional` until reviewed. A page carrying
`status: reviewed` SHALL mean the curator stands behind its stated significance,
whoever first drafted the prose. The `status` front-matter field SHALL be the sole
marker of that distinction; the body SHALL NOT carry an inline authorship
disclaimer, so that endorsement is a single front-matter change and no stale
disclaimer can survive review.

#### Scenario: Both sections are present

- **WHEN** a summary page is committed by any path
- **THEN** it contains a `## Summary` section and a `## Why this matters` section,
  each non-empty

#### Scenario: Commentary is solicited on the interactive path

- **WHEN** the user has not yet provided commentary during an interactive Phase 2
  interview
- **THEN** the LLM prompts for the user's "why this matters" before committing the
  summary page, and the committed page carries `status: reviewed`

#### Scenario: Drafted commentary is marked provisional

- **WHEN** a summary's `## Why this matters` is drafted by the LLM on the
  unattended path
- **THEN** the page carries `status: provisional` and its body contains no inline
  authorship disclaimer

#### Scenario: Endorsement is a single-field change

- **WHEN** the curator endorses a provisional page's drafted commentary as written
- **THEN** only its `status` changes to `reviewed`, with no body edit required

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

### Requirement: Tag vocabulary consistency at ingest

When proposing tags, both the interactive and unattended ingest paths SHALL prefer
tags already in use elsewhere in the wiki over minting new ones. On the interactive
path any newly-minted tag SHALL be surfaced explicitly for the user to approve or
redirect before the page is committed. On the **unattended path there is no
approver**, so tag approval is deferred rather than skipped: a newly-minted tag MAY
be committed, but the page carries `status: provisional` and the ingest's
`wiki/log.md` entry SHALL name every tag the run minted, so new vocabulary is
visible at review and can be redirected by `curate`. Corpus-wide reconciliation of
existing near-duplicate or orphan tags remains out of scope for ingest and is
handled by the `lint` command.

#### Scenario: Existing tags are preferred

- **WHEN** the LLM proposes tags for a new page on either path
- **THEN** it draws from the tags already used in the wiki where they apply,
  rather than inventing near-duplicate tags

#### Scenario: New tags are surfaced for approval on the interactive path

- **WHEN** the LLM proposes a tag not already present in the wiki during an
  interactive interview
- **THEN** it flags the tag as new so the user can approve or redirect it before
  commit

#### Scenario: Unattended new tags are logged for deferred approval

- **WHEN** the unattended path commits a page carrying a tag not already present
  in the wiki
- **THEN** the page carries `status: provisional` and that ingest's `wiki/log.md`
  entry names the newly-minted tag

#### Scenario: Deferred tag approval happens at review

- **WHEN** the curator reviews a provisional page that introduced a new tag
- **THEN** they can approve it or redirect it to an existing tag via `curate`'s
  retag verb

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

