# unattended-ingestion Specification

## Purpose

Drain the root `inbox.md` queue of sources into the wiki with no interview
present. This is the `ingest-inbox` command: it reuses the same `wiki-capture`
Phase 1 as the interactive `file` command, then authors Phase 2 pages on its own
judgment — classification, tags, hub links, figure decisions, and drafted
`## Why this matters` — committing them as ordinary pages, final as written.
Each entry succeeds or is parked independently, and already-ingested sources are
skipped, so re-runs are idempotent.

## Requirements
### Requirement: Inbox source queue

The wiki SHALL maintain a committed `inbox.md` file at the repository root as the
queue of sources awaiting unattended ingest. Each queue entry SHALL be a Markdown
checklist line carrying a URL or local path, optionally followed by a separator
and a free-text curator note. The file SHALL NOT live under `wiki/`, so that it is
neither published by the site build nor read as an untyped knowledge page by
`lint`. Entry state SHALL be recorded in the checkbox: unprocessed (`- [ ]`),
ingested (`- [x]`), parked awaiting the curator (`- [!]`), or dead or rejected
(`- [-]`). A `- [-]` entry needs no action and is never retried. The unattended
ingest command SHALL update these checkboxes in place and SHALL NOT delete entries.

#### Scenario: Curator queues a link with a note

- **WHEN** the curator appends `- [ ] <url> — <note>` to `inbox.md`
- **THEN** the entry is recognized as an unprocessed source with that note
  attached to it

#### Scenario: Ingested entry is checked off

- **WHEN** an unattended ingest successfully authors wiki pages for a queue entry
- **THEN** that entry's checkbox is marked `- [x]` in `inbox.md` and the entry
  text is retained

#### Scenario: Unprocessed entries only are considered

- **WHEN** an unattended ingest run scans `inbox.md`
- **THEN** it captures only `- [ ]` entries and `- [!]` entries whose drop file is
  present, and skips entries marked `- [x]` or `- [-]`

#### Scenario: Dead entry is never retried

- **WHEN** a run scans an inbox containing a `- [-]` entry
- **THEN** that entry is skipped and does not appear in the manual-fetch report

#### Scenario: Inbox is excluded from the published site

- **WHEN** the site is built
- **THEN** `inbox.md` is not published, because it resides outside `wiki/`

### Requirement: Unattended authoring without an interview

The unattended ingest path SHALL run Phase 1 capture unchanged and then author the
`wiki/` layer with no interactive interview: it SHALL determine the page type,
title, and tags, link to existing entity and concept hubs, create new hubs where
the source warrants them, and draft both body sections of the summary. It SHALL
have no interactive branches whatsoever, so that a headless run can never block on
a prompt. Any ambiguity SHALL resolve either to a documented default or to
skipping that entry with an annotation, never to a question. All other ingest
invariants SHALL be preserved: the `raw/` twin remains immutable, converter
routing is unchanged, and a page whose `type` falls outside the defined set is not
written.

Because this path drafts prose with no reviewer present, it SHALL apply the
corpus-independence constraint at the point of writing rather than relying on review
to catch a violation. In particular, when the unattended path observes that the corpus
does not yet cover something — a work it cannot link, a hub it declines to mint — it
SHALL record that observation in the run's `wiki/log.md` entry, which is exempt from
the constraint, and SHALL NOT write it into the page.

#### Scenario: Pages are authored with no prompt

- **WHEN** an unattended ingest processes a queue entry
- **THEN** the summary, hub, index, and log writes complete without any question
  being asked of a user

#### Scenario: Ambiguity does not block the run

- **WHEN** the unattended path encounters a decision it cannot resolve
- **THEN** it applies a documented default or skips the entry with an inbox
  annotation, and the run continues

#### Scenario: Raw twin remains immutable

- **WHEN** unattended authoring writes wiki pages for a captured source
- **THEN** no file under `raw/` is edited or renamed

#### Scenario: Drafted prose carries no corpus-membership claim

- **WHEN** the unattended path drafts a summary body or hub prose
- **THEN** the committed page contains no claim about what the wiki does or does not
  contain, and no corpus-scoped superlative or count

#### Scenario: A noticed gap goes to the log, not the page

- **WHEN** the unattended path determines that no existing page covers something the
  source references
- **THEN** that observation appears in the ingest's `wiki/log.md` entry and does not
  appear in any knowledge page

### Requirement: Curator note seeds drafted commentary

When a queue entry carries a curator note, the unattended path SHALL use that note
as the basis of the drafted `## Why this matters` section, preserving the curator's
stated reason for saving the source. When no note is present, the drafted section
SHALL be inferred from the source and its relationship to the existing corpus.

#### Scenario: Note anchors the drafted significance

- **WHEN** a queue entry includes a curator note and is ingested unattended
- **THEN** the drafted `## Why this matters` reflects that note

#### Scenario: Absent note falls back to corpus inference

- **WHEN** a queue entry has no curator note
- **THEN** the drafted `## Why this matters` is inferred from the source and its
  connections to existing wiki pages, and the page is still written

### Requirement: Per-entry failure isolation

Each queue entry SHALL be processed independently. A failure on one entry —
conversion failure, unreachable source, or authoring halt — SHALL NOT abort the
run or discard work already completed for other entries. A failed entry SHALL be
marked `- [!]` in `inbox.md` with the date, the reason, the acquisition attempts
already made, and a drop path, so that it is not retried on every subsequent run
while remaining visible to the curator. An entry judged not worth ingesting at all
SHALL instead be marked `- [-]` with the date and reason. The run SHALL report a
per-entry outcome summary on completion.

#### Scenario: One failure does not stop the batch

- **WHEN** conversion fails for one entry in a multi-entry run
- **THEN** the remaining entries are still processed and their pages are written

#### Scenario: Failed entry is parked with a reason

- **WHEN** an entry fails to convert
- **THEN** its inbox line is marked `- [!]` and annotated with the date, the failure
  reason, the attempts made, and a drop path of the form
  `→ drop: inbox-files/<slug>.<ext>`

#### Scenario: Parked entry is not retried

- **WHEN** a subsequent run scans an inbox containing a `- [!]` entry whose drop
  file is absent
- **THEN** that entry is skipped

#### Scenario: Out-of-scope source is marked dead

- **WHEN** an entry's capture succeeds but the source is judged outside the wiki's
  subject matter or not a single document
- **THEN** its line is marked `- [-]` with the date and reason, and no drop path is
  given

### Requirement: Duplicate sources are skipped

Before capturing an entry, the unattended path SHALL check whether the entry's URL
or path already appears as the `source:` of an existing summary page. If it does,
the path SHALL skip capture and authoring entirely, write no `raw/` twin, and mark
the entry `- [x]` with an annotation identifying it as already ingested.

YouTube video URLs SHALL be compared by video ID, not literal string.

#### Scenario: Already-ingested link is skipped

- **WHEN** a queue entry's URL matches the `source:` of an existing summary
- **THEN** no new `raw/` twin or `wiki/` page is written and the entry is checked
  off as already ingested

#### Scenario: Re-running a drained inbox is a no-op

- **WHEN** the unattended path runs against an inbox whose entries are all
  `- [x]` or `- [!]`
- **THEN** no files are created or modified under `raw/` or `wiki/`

#### Scenario: Different share link for an ingested video is skipped

- **WHEN** a queue entry is `https://youtu.be/<id>?si=<token>` and an existing summary
  has `source: https://www.youtube.com/watch?v=<id>`
- **THEN** the entry is treated as already ingested, no new `raw/` twin or `wiki/` page
  is written, and the entry is checked off naming the existing page

### Requirement: Implausible captures are refused

The unattended path SHALL refuse to author wiki pages from a captured twin whose
content is implausibly thin or is recognizably a cookie wall, paywall stub, login
page, or error page rather than the intended source. In that case it SHALL write
no `wiki/` pages and SHALL mark the entry `- [!]` with the reason and a drop path.
A stub that capture rejected mechanically leaves no twin; a twin that capture did
write and the unattended path then refuses SHALL be left in place, immutable.

#### Scenario: Paywall stub does not become a summary

- **WHEN** capture yields a twin that is a paywall or cookie-consent stub
- **THEN** no summary or hub page is written and the entry is parked with the
  reason and a drop path

#### Scenario: Refusal leaves the twin intact

- **WHEN** the unattended path refuses to author from a captured twin
- **THEN** the twin remains under `raw/` unmodified

#### Scenario: Mechanically rejected stub leaves no twin

- **WHEN** every acquisition attempt for an entry is rejected as a stub by capture
- **THEN** no twin is written under `raw/` and the entry is parked with the attempts
  and a drop path

### Requirement: Bookkeeping and autonomous publication

For each successfully ingested entry the unattended path SHALL update `index.md`
and append an entry to `wiki/log.md` identifying the run as unattended, then create
one git commit for that source. After processing all entries the run SHALL push
once to the default branch, so that the new pages publish to the live site
without human contact. Before pushing, the run SHALL rebase on the remote; on
conflict it SHALL abort the push, leave the commits local, and report the
conflict. It SHALL never force-push and SHALL never resolve a content conflict
unattended.

#### Scenario: Each source gets its own commit

- **WHEN** a run ingests several entries successfully
- **THEN** each ingested source is committed separately

#### Scenario: Batch pushes once

- **WHEN** a run completes with at least one successful ingest
- **THEN** it pushes once to the default branch, triggering the site deploy

#### Scenario: Log marks the run as unattended

- **WHEN** an unattended ingest is logged
- **THEN** the appended `wiki/log.md` entry identifies it as unattended, without
  rewriting existing entries

#### Scenario: Push conflict aborts safely

- **WHEN** the remote has diverged such that rebasing before the push conflicts
- **THEN** the push is abandoned, the commits remain local, the conflict is
  reported, and no force-push occurs

### Requirement: Drop path for a parked entry

Every `- [!]` entry the unattended path writes SHALL name one drop path under
`inbox-files/`, whose stem is the slug of the best title known for the source and
whose extension names the expected format. A file at that stem with any extension
SHALL satisfy the drop.

#### Scenario: Drop path is named from the paper's title

- **WHEN** an ACM entry is parked and the open-access lookup learned the title
  "A Nanopass Framework for Commercial Compiler Development"
- **THEN** the drop path is
  `inbox-files/a-nanopass-framework-for-commercial-compiler-development.pdf`

#### Scenario: Assembled Markdown satisfies a PDF drop path

- **WHEN** the drop path ends in `.pdf` and the curator places a `.md` file with the
  same stem
- **THEN** the drop is considered present

### Requirement: Parked entries resolve from a dropped file

When a `- [!]` entry's drop file is present, the unattended path SHALL capture that
file under the entry's original URL, author pages as for any entry, and mark the
**same line** `- [x]`, keeping its note and park reason and appending the date and
that it was resolved from the drop. It SHALL NOT add a new inbox line.

#### Scenario: Dropped PDF resolves its parked line

- **WHEN** `inbox-files/implicit-phasing-for-r6rs-libraries.pdf` exists and the
  inbox holds `- [!] https://legacy.cs.indiana.edu/~dyb/pubs/implicit-phasing.pdf …
  → drop: inbox-files/implicit-phasing-for-r6rs-libraries.pdf`
- **THEN** the summary's `source:` is the `legacy.cs.indiana.edu` URL, the line
  becomes `- [x]` with its prior text kept, and no new line is appended

#### Scenario: Dropped file for an already-ingested URL is a duplicate

- **WHEN** a parked entry's drop file is present but a summary already has the
  entry's URL as its `source:`
- **THEN** nothing is captured and the line is marked `- [x]` naming the existing
  page

### Requirement: Manual-fetch report

Each unattended run SHALL end its outcome summary with the list of `- [!]` entries
whose drop file is still absent, giving for each the source URL and the drop path.
The same list SHALL be obtainable on demand without running an ingest and without
network access. When the curator has configured a library proxy prefix, each URL in
the list SHALL also be shown through that proxy.

#### Scenario: Run ends with the pending list

- **WHEN** a run finishes and two `- [!]` entries have no drop file
- **THEN** the outcome summary lists both, each with its URL and drop path

#### Scenario: Pending list on demand

- **WHEN** the curator asks for the pending list
- **THEN** it is printed from `inbox.md` alone, with no capture and no network
  request

#### Scenario: Proxy links when configured

- **WHEN** a library proxy prefix is configured
- **THEN** each pending entry also shows its URL prefixed by that proxy
