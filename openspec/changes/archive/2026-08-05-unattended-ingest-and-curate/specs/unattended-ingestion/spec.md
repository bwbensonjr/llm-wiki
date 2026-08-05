## ADDED Requirements

### Requirement: Inbox source queue

The wiki SHALL maintain a committed `inbox.md` file at the repository root as the
queue of sources awaiting unattended ingest. Each queue entry SHALL be a Markdown
checklist line carrying a URL or local path, optionally followed by a separator
and a free-text curator note. The file SHALL NOT live under `wiki/`, so that it is
neither published by the site build nor read as an untyped knowledge page by
`lint`. Entry state SHALL be recorded in the checkbox: unprocessed (`- [ ]`),
ingested (`- [x]`), or parked after failure (`- [!]`). The unattended ingest
command SHALL update these checkboxes in place and SHALL NOT delete entries.

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
- **THEN** it processes only `- [ ]` entries and skips entries already marked
  `- [x]` or `- [!]`

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

### Requirement: Unattended writes are provisional

Every `wiki/` knowledge page written by the unattended path SHALL carry
`status: provisional`. A hub page that the unattended path creates SHALL be
written `status: provisional`. A hub page already carrying `status: reviewed` that
the unattended path merely appends a source backlink to SHALL retain
`status: reviewed`, so that settled hubs are not returned to the review queue by
routine linking.

#### Scenario: Unattended summary is provisional

- **WHEN** the unattended path commits a summary page
- **THEN** the page's front-matter carries `status: provisional`

#### Scenario: Newly created hub is provisional

- **WHEN** the unattended path creates an entity or concept hub that did not exist
- **THEN** that hub is written with `status: provisional`

#### Scenario: Reviewed hub is not reverted

- **WHEN** the unattended path appends a source backlink to a hub whose status is
  `reviewed`
- **THEN** that hub's status remains `reviewed`

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
  `status: provisional`

### Requirement: Per-entry failure isolation

Each queue entry SHALL be processed independently. A failure on one entry —
conversion failure, unreachable source, or authoring halt — SHALL NOT abort the
run or discard work already completed for other entries. A failed entry SHALL be
marked `- [!]` in `inbox.md` with the date and the reason, so that it is not
retried on every subsequent run while remaining visible to the curator. The run
SHALL report a per-entry outcome summary on completion.

#### Scenario: One failure does not stop the batch

- **WHEN** conversion fails for one entry in a multi-entry run
- **THEN** the remaining entries are still processed and their pages are written

#### Scenario: Failed entry is parked with a reason

- **WHEN** an entry fails to convert
- **THEN** its inbox line is marked `- [!]` and annotated with the date and
  failure reason

#### Scenario: Parked entry is not retried

- **WHEN** a subsequent run scans an inbox containing a `- [!]` entry
- **THEN** that entry is skipped

### Requirement: Duplicate sources are skipped

Before capturing an entry, the unattended path SHALL check whether the entry's URL
or path already appears as the `source:` of an existing summary page. If it does,
the path SHALL skip capture and authoring entirely, write no `raw/` twin, and mark
the entry `- [x]` with an annotation identifying it as already ingested.

#### Scenario: Already-ingested link is skipped

- **WHEN** a queue entry's URL matches the `source:` of an existing summary
- **THEN** no new `raw/` twin or `wiki/` page is written and the entry is checked
  off as already ingested

#### Scenario: Re-running a drained inbox is a no-op

- **WHEN** the unattended path runs against an inbox whose entries are all
  `- [x]` or `- [!]`
- **THEN** no files are created or modified under `raw/` or `wiki/`

### Requirement: Implausible captures are refused

The unattended path SHALL refuse to author wiki pages from a captured twin whose
content is implausibly thin or is recognizably a cookie wall, paywall stub, login
page, or error page rather than the intended source. In that case it SHALL write
no `wiki/` pages and SHALL mark the entry `- [!]` with the reason. The `raw/` twin
that capture already produced SHALL be left in place, immutable.

#### Scenario: Paywall stub does not become a summary

- **WHEN** capture yields a twin that is a paywall or cookie-consent stub
- **THEN** no summary or hub page is written and the entry is parked with the
  reason

#### Scenario: Refusal leaves the twin intact

- **WHEN** the unattended path refuses to author from a captured twin
- **THEN** the twin remains under `raw/` unmodified

### Requirement: Bookkeeping and autonomous publication

For each successfully ingested entry the unattended path SHALL update `index.md`
and append an entry to `wiki/log.md` identifying the run as unattended, then create
one git commit for that source. After processing all entries the run SHALL push
once to the default branch, so that provisional pages publish to the live site
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
