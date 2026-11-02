# Proposal

## Why

Pages ingested unattended from `inbox.md` are written `status: provisional` and
wait in a review queue for `/curate`. In practice that review step adds
ceremony without adding value: the curator's note on the inbox line already
carries their judgment, and the provisional/reviewed split leaves a field on
every page and a whole command to maintain. Ingested pages should simply be
pages.

## What Changes

- **BREAKING** Remove the `status` front-matter field from the page taxonomy.
  No page carries it and no command writes or validates it.
- Unattended ingest (`/ingest-inbox`) writes ordinary pages. Its own judgment
  calls (classification, tags, figures, drafted `## Why this matters`) are
  final as committed, the same as an interactive `/file` commit.
- **BREAKING** Remove the `curate` command and the `corpus-curation`
  capability: the provisional queue, the review verbs (endorse, retag,
  reclassify, merge hub, reject), and duplicate-hub clustering.
- New tags minted unattended are still named in the run's `wiki/log.md`
  entry, so they remain visible. Cleanup of near-duplicate tags stays `lint`'s
  job.
- The corpus-independence rule stays. Correcting a stale corpus-membership
  claim, the one permitted later edit to a summary, becomes an ordinary
  curator edit rather than a `curate` verb.
- One-time migration: strip the `status:` line from every existing page in
  `wiki/` (17 provisional, 118 reviewed). `wiki/log.md` history stays as
  written.
- Update `CLAUDE.md`, `README.md`, `inbox.md`, the page templates, and the
  `ingest-inbox` and `lint` skills. Delete `.claude/skills/curate/`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `resource-ingestion`: remove `status` from the page taxonomy; `## Why this
  matters` is no longer endorsement-gated; unattended new tags are logged
  without a deferred-approval step; the corpus-independence correction becomes
  a curator edit.
- `unattended-ingestion`: remove the "Unattended writes are provisional"
  requirement and provisional/curate references from the remaining
  requirements.
- `image-capture`: unattended figure decisions are logged but no longer
  "reviewable and reversible via `curate`".
- `corpus-curation`: removed in full.

## Impact

- Skills: `.claude/skills/curate/` deleted; `.claude/skills/ingest-inbox/SKILL.md`
  and `.claude/skills/lint/SKILL.md` edited.
- Docs and conventions: `CLAUDE.md`, `README.md`, `inbox.md`, `templates/*.md`.
- Content: front-matter of every `wiki/` knowledge page (one-line removal).
- `raw/`, the capture CLI, and the publish pipeline are unaffected.
