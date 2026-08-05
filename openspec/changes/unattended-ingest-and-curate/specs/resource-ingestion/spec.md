## MODIFIED Requirements

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
