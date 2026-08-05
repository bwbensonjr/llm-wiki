# corpus-curation Specification

## Purpose

Review the queue of machine-authored, `status: provisional` wiki pages and
exercise the judgment the unattended ingest path deferred — endorsing,
correcting, retagging, reclassifying, merging, and rejecting them. This is the
`curate` command. It is the "review after the write" half of the decoupled
capture/review cadence: it moves human judgment after the commit rather than
removing it. It is deliberately orthogonal to `lint`, which audits structure and
repairs; `curate` exercises judgment and never repairs a structural defect it
happens to notice.

## Requirements
### Requirement: Review queue is derived from front-matter

The `curate` command SHALL determine its review queue by scanning the `status:`
front-matter field of `wiki/` knowledge pages, treating every page carrying
`status: provisional` as awaiting review. It SHALL NOT maintain a separate queue
file, so the queue can never drift from the corpus. Because the queue is derived
from durable page state, an interrupted or partially-completed review SHALL leave
the unreviewed remainder in the queue for the next run.

#### Scenario: Provisional pages form the queue

- **WHEN** the curator runs `curate`
- **THEN** the pages presented for review are exactly those carrying
  `status: provisional`

#### Scenario: Interrupted review resumes

- **WHEN** a previous `curate` run endorsed some pages and was abandoned before
  reaching others
- **THEN** the next run presents the still-provisional pages and omits the
  endorsed ones

#### Scenario: Empty queue reports nothing to review

- **WHEN** no page carries `status: provisional`
- **THEN** the command reports an empty queue and proposes no changes

### Requirement: Read-only survey by default

The `curate` command SHALL survey the queue and report it without writing any
files by default. Running `curate` to inspect what is awaiting review SHALL leave
`wiki/`, `raw/`, `inbox.md`, and all bookkeeping files unchanged. The report SHALL
identify each queued page by filename and SHALL state the queue's size and the age
of its oldest entry, so that accumulating review debt is visible rather than
silent.

#### Scenario: Survey writes nothing

- **WHEN** the curator runs `curate` and commits no decision
- **THEN** no file under `wiki/`, `raw/`, or `inbox.md` is created, modified, or
  deleted

#### Scenario: Queue debt is reported

- **WHEN** the command reports the queue
- **THEN** it states how many pages await review and how old the oldest is

### Requirement: Review is presented with corpus-relational context

For each queued page the `curate` command SHALL present, in addition to the page's
own drafted content, its relationship to the existing corpus: which hubs it links
to, which existing pages it duplicates or overlaps, and which it contradicts or
extends. It SHALL additionally flag any tag the page carries that is new to the
corpus, so that the tag approval deferred at unattended ingest happens here.
Presentation SHALL NOT consist solely of restating the drafted page, so that review
is a judgment prompt rather than an approval queue.

#### Scenario: Connections are surfaced with the page

- **WHEN** a provisional summary is presented for review
- **THEN** the presentation includes the corpus pages it relates to, not only its
  own drafted text

#### Scenario: Newly minted tags are flagged at review

- **WHEN** a provisional page carries a tag introduced by the unattended path
- **THEN** the command flags that tag as new so the curator can approve it or
  redirect it via the retag verb

#### Scenario: Overlap with an existing page is flagged

- **WHEN** a provisional page substantially overlaps an existing summary
- **THEN** the command flags the overlap during review

### Requirement: Review verbs

The `curate` command SHALL offer the following decisions for each queued page:
**endorse** (accept as written), **edit-then-endorse** (revise the body, including
replacing drafted `## Why this matters` prose with the curator's own, then
accept), **retag** (adjust `tags:`), **reclassify** (change `type` and re-file the
page into the folder mirroring the new type), **merge hub** (fold a provisional hub
into an existing one), and **reject** (remove the page). Endorsing a page SHALL set
its `status` to `reviewed`. A page left undecided SHALL remain `provisional`.

#### Scenario: Endorsement flips status

- **WHEN** the curator endorses a provisional page and commits
- **THEN** that page's `status` becomes `reviewed` and its other front-matter and
  body are otherwise unchanged

#### Scenario: Curator replaces the drafted commentary

- **WHEN** the curator rewrites a page's `## Why this matters` during review and
  endorses it
- **THEN** the committed page carries the curator's prose and `status: reviewed`

#### Scenario: Reclassification re-files the page

- **WHEN** the curator changes a page's `type` during review
- **THEN** the page is moved into the folder mirroring its new `type` and its
  `index.md` grouping is corrected

#### Scenario: Undecided page stays in the queue

- **WHEN** the curator makes no decision about a queued page
- **THEN** that page retains `status: provisional` and appears in the next run's
  queue

### Requirement: Duplicate hub clustering

The `curate` command SHALL cluster provisional hub pages that appear to name the
same entity or concept as one another or as an existing hub — including slug
variants differing by casing, punctuation, name form, abbreviation, or
pluralization — and SHALL propose a canonical page for each cluster. It SHALL NOT
merge hubs on its own; the choice of canonical page and which variants fold into it
SHALL be a curator decision. On an approved merge the command SHALL redirect every
`[[wikilink]]` that pointed at a folded variant to the canonical page, move that
variant's Sources backlinks onto the canonical page, delete the variant, and update
`index.md`.

#### Scenario: Slug variants are clustered

- **WHEN** the queue contains a provisional hub whose slug is a name-form or
  casing variant of an existing hub
- **THEN** the command clusters them and proposes a canonical page for the curator
  to confirm

#### Scenario: Merges require approval

- **WHEN** the command proposes folding a provisional hub into an existing one
- **THEN** no page is deleted or rewritten until the curator approves the merge

#### Scenario: Approved merge redirects inbound links

- **WHEN** the curator approves folding a variant hub into a canonical page
- **THEN** every `[[wikilink]]` targeting the variant is rewritten to the
  canonical page, the variant's Sources backlinks are carried over, the variant
  file is deleted, and `index.md` is updated

### Requirement: Rejection deletes without a tombstone

Rejecting a page SHALL delete that page's file, remove its entry from
`wiki/index.md`, and remove its backlink from every hub that cites it. Any hub
created solely by the rejected page's ingest and left with no remaining sources
SHALL also be deleted. No tombstone or placeholder page SHALL be left behind; the
`wiki/log.md` entry and git history are the record. The rejected source's `raw/`
twin and any `raw/assets/` bytes SHALL be retained, immutable, so the rejection is
recoverable without refetching. If the rejected summary had promoted a figure into
`wiki/assets/`, that promoted copy SHALL be removed while the `raw/assets/`
original remains.

#### Scenario: Rejected page is fully unlinked

- **WHEN** the curator rejects a provisional summary and commits
- **THEN** the page file is deleted, its `index.md` entry is removed, and no hub
  retains a backlink to it

#### Scenario: Hub orphaned by rejection is removed

- **WHEN** a rejected summary was the only source of a hub created by its ingest
- **THEN** that hub is deleted as well

#### Scenario: Raw twin survives rejection

- **WHEN** a page is rejected
- **THEN** its `raw/` twin and `raw/assets/` bytes remain on disk unmodified

#### Scenario: No tombstone page is written

- **WHEN** a page is rejected
- **THEN** no placeholder or tombstone page is created in its place

### Requirement: Decisions are curator-gated and logged

The `curate` command SHALL apply decisions through a propose → coach → commit
interview: it SHALL preview the intended changes, allow the curator to revise them,
and write nothing unless the curator commits. It SHALL never edit or rename a file
under `raw/`. On commit it SHALL append one `## [<date>] curate: <subject>` entry
to `wiki/log.md` without rewriting existing entries, recording what was endorsed,
merged, and rejected, including the reason for each rejection.

#### Scenario: Decisions apply only on commit

- **WHEN** the command proposes decisions and the curator does not commit
- **THEN** the wiki is left unchanged

#### Scenario: raw twins are never modified

- **WHEN** `curate` applies any decision
- **THEN** no file under `raw/` is edited or renamed

#### Scenario: Committed run is logged

- **WHEN** the curator commits one or more decisions
- **THEN** a single `## [<date>] curate: <subject>` entry is appended to
  `wiki/log.md` naming what was endorsed, merged, and rejected, with rejection
  reasons

### Requirement: Curation is distinct from linting

The `curate` command SHALL restrict itself to review of the provisional queue and
SHALL NOT report or repair structural defects, which remain the `lint` command's
responsibility. Correspondingly, a page carrying `status: provisional` SHALL NOT be
treated as a defect by `lint`, so that a corpus of unreviewed pages still reports
as structurally clean.

#### Scenario: Provisional status is not a lint defect

- **WHEN** `lint` audits a corpus containing provisional pages that are otherwise
  well-formed
- **THEN** it reports a clean result and does not list them as defects

#### Scenario: Curate does not repair structure

- **WHEN** `curate` encounters a structural defect such as a broken wikilink
- **THEN** it does not repair it as part of review, leaving it to `lint`
