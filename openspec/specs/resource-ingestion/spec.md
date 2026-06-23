# resource-ingestion Specification

## Purpose
TBD - created by archiving change add-resource-ingestion. Update Purpose after archive.
## Requirements
### Requirement: Wiki page taxonomy

The wiki SHALL classify every knowledge page with a `type` front-matter field
whose value is one of `summary`, `entity`, `concept`, or `analysis`, following
Karpathy's content-oriented classification. The wiki SHALL additionally maintain
two bookkeeping files: `index.md` (a catalog) and `log.md` (an append-only
timeline). Knowledge pages SHALL be stored under `wiki/` in a folder matching
their type (`wiki/summaries/`, `wiki/entities/`, `wiki/concepts/`,
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
conversion accordingly: web URLs to Jina Reader, PDFs to Docling, and all other
file types to MarkItDown. Detection SHALL consider the fetched content type, not
the file extension alone, so that a URL resolving to a PDF is routed to Docling.

#### Scenario: Web URL routes to Jina Reader

- **WHEN** the user files an `http(s)` URL that resolves to an HTML page
- **THEN** the resource is converted with Jina Reader

#### Scenario: PDF routes to Docling

- **WHEN** the user files a PDF, whether a local path or a URL resolving to PDF
  content
- **THEN** the resource is converted with Docling

#### Scenario: Other file types route to MarkItDown

- **WHEN** the user files a non-PDF document such as `.docx`, `.pptx`, `.xlsx`,
  or an image
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

A `summary` page SHALL carry two distinct voices: a `## Summary` section
containing the LLM's neutral distillation of the source, and a `## Why this
matters` section containing the user's own commentary on why the resource is
interesting, collected during the Phase 2 interview.

#### Scenario: Both voices are captured

- **WHEN** a summary page is committed
- **THEN** it contains a `## Summary` section authored by the LLM and a `## Why
  this matters` section authored from the user's commentary

#### Scenario: Commentary is solicited during the interview

- **WHEN** the user has not yet provided commentary in Phase 2
- **THEN** the LLM prompts for the user's "why this matters" before committing
  the summary page

### Requirement: Tag vocabulary consistency at ingest

When proposing tags during the Phase 2 interview, the `file` command SHALL
prefer tags already in use elsewhere in the wiki over minting new ones. Any
newly-minted tag SHALL be surfaced explicitly for the user to approve or
redirect before the page is committed. Corpus-wide reconciliation of existing
near-duplicate or orphan tags is out of scope for this command and is deferred
to the future `lint` command.

#### Scenario: Existing tags are preferred

- **WHEN** the LLM proposes tags for a new page
- **THEN** it draws from the tags already used in the wiki where they apply,
  rather than inventing near-duplicate tags

#### Scenario: New tags are surfaced for approval

- **WHEN** the LLM proposes a tag not already present in the wiki
- **THEN** it flags the tag as new during the interview so the user can approve
  or redirect it before commit

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

