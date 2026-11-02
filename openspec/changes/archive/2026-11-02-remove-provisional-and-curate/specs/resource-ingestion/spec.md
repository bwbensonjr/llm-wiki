# Spec Delta

## ADDED Requirements

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

## MODIFIED Requirements

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

## REMOVED Requirements

### Requirement: Wiki page taxonomy

**Reason**: Its `status` field (`provisional | reviewed`) and the scenarios
built on it are removed along with the review queue.

**Migration**: Replaced by "Knowledge page classification" (the `type`
taxonomy, folders, and bookkeeping files, unchanged) and "Pages carry no review
status". Existing pages have their `status:` line removed.

### Requirement: Dual-voice summary pages

**Reason**: The endorsement gate on `## Why this matters` depended on the
`status` field, which is removed.

**Migration**: Replaced by "Two-section summary pages", which keeps both
sections and the no-disclaimer rule.

### Requirement: Tag vocabulary consistency at ingest

**Reason**: Deferred tag approval through `curate`'s retag verb is removed with
the `curate` command.

**Migration**: Replaced by "Tag vocabulary preference at ingest". Unattended new
tags are still logged; near-duplicate cleanup stays with `lint`.
