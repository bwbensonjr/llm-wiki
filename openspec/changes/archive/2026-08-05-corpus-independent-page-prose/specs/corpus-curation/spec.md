## MODIFIED Requirements

### Requirement: Review verbs

The `curate` command SHALL offer the following decisions for each queued page:
**endorse** (accept as written), **edit-then-endorse** (revise the body, including
replacing drafted `## Why this matters` prose with the curator's own, then
accept), **retag** (adjust `tags:`), **reclassify** (change `type` and re-file the
page into the folder mirroring the new type), **merge hub** (fold a provisional hub
into an existing one), and **reject** (remove the page). Endorsing a page SHALL set
its `status` to `reviewed`. A page left undecided SHALL remain `provisional`.

A claim that violates the corpus-independence constraint SHALL be correctable under
**edit-then-endorse**, and SHALL be correctable on a page already carrying
`status: reviewed`. This is a deliberate exception to the ordinary rule that `curate`
acts on the provisional queue: such a claim is true when written and becomes false
later, so the page that needs correcting is frequently one the curator has already
endorsed. Correcting it SHALL leave `status: reviewed` unchanged rather than returning
the page to the queue.

Correcting a summary in this way SHALL also be permitted despite summaries being
written once at ingest. That permission is narrow: it extends only to removing or
rephrasing the offending claim, and SHALL NOT be used to revise the distillation.

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

#### Scenario: Stale corpus claim is corrected on a reviewed page

- **WHEN** the curator finds a corpus-membership claim on a page carrying
  `status: reviewed`
- **THEN** the claim is removed or rephrased and the page remains `status: reviewed`

#### Scenario: Summary correction is limited to the offending claim

- **WHEN** the curator corrects a corpus-membership claim in a `summary` page
- **THEN** only that claim is removed or rephrased and the surrounding distillation is
  left as written
