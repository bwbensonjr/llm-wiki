## Why

The wiki can now ingest sources (`file`) and answer questions against them
(`query`), but nothing keeps the corpus *internally consistent* as it grows.
`file` and `query` each defer corpus-wide hygiene to a future `lint` command:
tag reconciliation is "the future `lint` command's job, not ingest's," and
"index maintenance/repair is `lint`'s concern." Today a broken `[[wikilink]]`, a
page missing from `index.md`, a near-duplicate tag, or a page in the wrong
folder for its `type` can only be caught by hand. `lint` is the last planned
command — it audits the whole corpus for these defects and, under curator
gating, repairs them.

## What Changes

- Add a `lint` command (an LLM skill, `.claude/skills/lint/SKILL.md`) that
  audits the entire `wiki/` corpus for structural and consistency defects and
  reports them, **writing nothing by default**.
- **Diagnose across categories:** invalid or incomplete front-matter, `type`
  / folder mismatches, broken `[[wikilinks]]`, orphan pages, pages missing from
  or stale in `wiki/index.md`, missing body sections, and a near-duplicate /
  inconsistent **tag vocabulary** surfaced corpus-wide.
- **Report first, fix second (and optional):** after the report, the command
  offers a propose → coach → commit interview to apply repairs, separating
  mechanical fixes (re-file a misplaced page, restore a missing index entry)
  from judgment calls (which tags to merge into a canonical vocabulary). It
  writes to the wiki only on commit and previews changes as a diff first.
- **`raw/` stays immutable:** `lint` audits and may rewrite `wiki/` pages and
  bookkeeping files, but never edits or renames a `raw/` twin.
- **Bookkeeping symmetry:** a committed lint run appends one
  `## [<date>] lint: <subject>` entry to `wiki/log.md` and reflects any page
  moves/renames in `wiki/index.md`.

## Capabilities

### New Capabilities
- `corpus-lint`: auditing the whole wiki corpus for front-matter/taxonomy
  validity, link and index integrity, missing body sections, and tag-vocabulary
  consistency — reporting findings read-only by default and applying repairs
  only under a curator-gated commit.

### Modified Capabilities
<!-- resource-ingestion and corpus-query already DEFER corpus-wide tag
     reconciliation and index repair to `lint`. This change fulfills that
     deferral rather than changing those specs' requirements. No existing
     requirements change. -->
- _None._

## Impact

- **New skill:** `.claude/skills/lint/SKILL.md`.
- **New spec:** `openspec/specs/corpus-lint/spec.md` (via this change's delta).
- **Docs:** `README.md` and the command roadmap note `lint` as implemented,
  completing the capture → query → lint set.
- **Wiki content:** `lint` may rewrite `wiki/` pages, `index.md`, and `log.md`
  on commit (the first command to mutate existing pages in bulk); `raw/` is
  never touched.
- **No Python CLI changes:** auditing is LLM-driven reading/grepping over local
  Markdown, so no converter or `wiki_ingest` work is required — same rationale
  as `query`.
