## Why

Wiki pages currently assert things about *the corpus* whose truth changes every time a
source is ingested. A hub page reading "neither of which is itself an ingested source"
was factually correct when written and false hours later; it was corrected once and the
same sentence pattern broke again the same day. Because a page's prose is written once
and the corpus grows continuously, any claim about what the wiki does or does not
contain is a latent defect with a delayed trigger — and nothing in the system detects
it, because a stale claim is grammatically fine and links resolve normally.

The unattended ingest path makes this compounding rather than incidental. It drafts
prose with no reviewer present, at whatever cadence the inbox is filled, so a phrasing
habit becomes a corpus-wide property faster than review can catch it.

## What Changes

- Establish a **corpus-independence** rule for knowledge-page prose: a page describes
  its subject, and never asserts what the wiki contains, lacks, or ranks first among.
  Two banned classes:
  - **Presence/absence claims** — "X is not an ingested source", "no ingested source
    covers Y", "this is the corpus's first page on Z".
  - **Corpus-dependent superlatives and counts** — "the corpus's only measurement of
    that trade-off", "several pages here mentioned him before he had a page of his
    own". These carry the same staleness bug in less obvious grammar.
- **Explicitly preserve neutral sibling orientation.** Situating a subject among
  related pages — "sits in this wiki's collection of Scheme implementations alongside
  libscheme and Racket" — stays allowed. It is stable under growth (a new sibling does
  not falsify it) and it is a large part of what makes a hub worth reading. This
  boundary is the substance of the change; a rule that banned all self-reference would
  make hub pages worse.
- Bind the rule on both authoring paths — the interactive `file` interview and the
  unattended `ingest-inbox` run — so it constrains drafted prose at the point of
  writing rather than only at review.
- Give `curate` the standing to correct a violation it encounters, and make the
  correction shape explicit (restate the claim about the subject, drop the claim about
  the corpus).
- Remediate the existing corpus: 2 hard presence/absence claims and roughly 19 pages
  carrying softer corpus-dependent phrasing.

Not a `lint` concern. Detecting these claims requires reading prose for meaning, which
is judgment rather than structure, and `lint`'s contract is that a clean corpus reports
no defects. A phrase-matching heuristic would produce false positives on exactly the
sibling-orientation sentences this change protects.

## Capabilities

### New Capabilities

None. This constrains prose that existing capabilities already produce; introducing a
capability for a writing rule would fragment requirements that belong with the pages
they govern.

### Modified Capabilities

- `resource-ingestion`: the dual-voice summary and page-taxonomy requirements gain the
  corpus-independence constraint on authored page bodies, applying to summaries and
  hubs on both paths.
- `unattended-ingestion`: the unattended-authoring requirement gains the same
  constraint explicitly, since that path drafts `## Why this matters` and hub prose
  with no reviewer to catch a stale claim.
- `corpus-curation`: the review-verbs requirement gains corpus-dependent prose as a
  thing `curate` may correct under edit-then-endorse, including on a page whose
  `status` is already `reviewed`.

## Impact

- **Specs**: delta specs for the three capabilities above.
- **`CLAUDE.md`**: a convention passage stating the rule and the preserved boundary.
  Binding on every operation that reads or writes wiki content, so this is the primary
  surface.
- **Skills**: `.claude/skills/file/`, `.claude/skills/ingest-inbox/` (authoring), and
  `.claude/skills/curate/` (correction). No change to `.claude/skills/lint/`.
- **Corpus**: `wiki/entities/william-clinger.md` and
  `wiki/summaries/a-nanopass-framework-for-commercial-compiler-development.md` carry
  the hard violations; ~19 further pages carry superlative or count phrasing. Summaries
  are normally written once at ingest, so editing them for remediation is a deliberate
  exception this change has to authorize.
- **No code**: `wiki_ingest/` is untouched; this is entirely a content-authoring
  convention.
