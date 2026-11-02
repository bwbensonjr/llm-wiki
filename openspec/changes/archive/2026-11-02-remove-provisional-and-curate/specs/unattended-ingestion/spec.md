# Spec Delta

## MODIFIED Requirements

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

## REMOVED Requirements

### Requirement: Unattended writes are provisional

**Reason**: The `status` field and the review queue are removed. Pages written
unattended are ordinary pages, final as committed, the same as pages committed
through the interactive `file` interview.

**Migration**: Existing pages have their `status:` front-matter line removed by
this change. Corrections to an unattended page are made as ordinary curator
edits, or by re-filing the source interactively.
