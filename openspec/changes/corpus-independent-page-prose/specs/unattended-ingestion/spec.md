## MODIFIED Requirements

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
