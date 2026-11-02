# Design

## Context

`status: provisional | reviewed` is written by `ingest-inbox` (provisional),
`file` and `query` (reviewed, via the templates), and read only by `curate`,
which builds its queue from it. `lint` does not validate it, and nothing else
depends on it. Today 17 pages are provisional and 118 are reviewed.
`wiki/log.md` contains `ingest` and `curate` entries that talk about
provisional pages and curate runs.

## Goals / Non-Goals

**Goals:**
- No page, template, skill, or convention refers to `status` or `curate`
  (except as history).
- One mechanical migration commit that strips `status:` from existing pages.

**Non-Goals:**
- Re-reviewing the 17 provisional pages. They keep their content as written.
- Replacing `curate`'s hub-merge or reject verbs with a new command. Those
  become ordinary edits.
- Adding a `lint` check for a leftover `status` field. After the migration,
  nothing writes one.

## Decisions

- **Remove the field rather than keep it fixed at `reviewed`.** A field with
  one allowed value carries no information. The user chose removal.
- **Leave history alone.** `wiki/log.md` is append-only and exempt from
  corpus-independence, so its `curate` entries and provisional mentions stay.
  The `curate` op stays readable in old entries but leaves the live
  vocabulary. Page prose that recounts a past `curate` run (for example the
  `## Why this matters` of the nanopass summary) describes a real event and
  stays.
- **Keep "unattended" logging.** `ingest-inbox` still names the run as
  unattended and still logs minted tags and figure decisions. These are now a
  record, not a review queue.
- **Keep `lint` skipping `log.md` for broken links.** Logged links can still
  break when pages are renamed or deleted by hand. Only the explanation in
  `CLAUDE.md` and the `lint` skill changes, so it no longer cites `curate`.
- **Spec shape.** OpenSpec cannot drop scenarios from a MODIFIED requirement,
  so the three resource-ingestion requirements whose scenarios depended on
  `status` are REMOVED and replaced with renamed ADDED requirements. The
  `corpus-curation` capability is removed requirement by requirement.
- **No `wiki/log.md` entry for the migration.** It is not one of the logged
  operations (`ingest`, `query`, `lint`), and git history records it.
- **Migration by script, not by hand.** Delete exactly the
  `^status: (provisional|reviewed)$` line inside each page's front-matter
  block. Changing only that line makes the diff easy to audit.

## Risks / Trade-offs

- [The 17 provisional pages may contain judgment errors the curator never
  checked] → They are flagged in history (`wiki/log.md` ingest entries) and
  can be fixed by hand. List them in the migration commit message.
- [Losing duplicate-hub detection] → Near-duplicate tags stay with `lint`.
  Duplicate hubs are rare because ingest prefers existing hubs, and they can be
  merged by hand when noticed.
- [Archiving `corpus-curation` may leave an empty main spec] → Delete
  `openspec/specs/corpus-curation/` after archive if it remains.

## Migration Plan

1. Update conventions, templates, and skills; delete the `curate` skill.
2. Run the front-matter strip over `wiki/`, verify that no `status:` line
   remains and that YAML still parses, then commit.
3. Push; the publish workflow rebuilds the site (front-matter `status` was
   never rendered, so the site is unchanged).

Rollback is `git revert` of the change's commits.
