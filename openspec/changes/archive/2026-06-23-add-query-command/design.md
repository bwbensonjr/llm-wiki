## Context

The wiki today is write-only: the `file` command (skill + `wiki-capture` Python
CLI) ingests sources into immutable `raw/` twins and curator-authored `wiki/`
pages. The taxonomy already reserves a fourth page type, `analysis` — "a
filed-back query answer or comparison" — and an empty `wiki/analyses/` folder,
but nothing produces it. There is no `analysis` template and no front-matter
schema for it in `CLAUDE.md`.

`query` is the second of the planned commands (capture done; query + lint next).
It mirrors the established shape of `file`: a two-phase, curator-gated operation
authored as a Claude Code skill. The key difference is that `file`'s Phase 1 is
mechanical conversion (hence a Python CLI), whereas `query`'s "Phase 1" is
*retrieval and synthesis over local Markdown* — work the LLM does directly. So
`query` is a skill-only command with no Python counterpart.

## Goals / Non-Goals

**Goals:**

- Answer natural-language questions grounded in the wiki corpus, with
  `[[wikilink]]` citations back to the pages used.
- Be honest about coverage: never pass outside knowledge off as corpus-backed;
  say when the wiki does not cover something.
- Make filing optional and curator-gated, reusing the propose → coach → commit
  pattern from `file` so a quick lookup costs nothing and a filed answer is a
  first-class, cross-linked `analysis` page.
- Define the `analysis` page contract (template + front-matter) so the type that
  the taxonomy already names becomes real.

**Non-Goals:**

- No embeddings, vector index, or external search service. Retrieval is
  index-first reading of local Markdown.
- No Python/CLI changes; `wiki_ingest` and `wiki-capture` are untouched.
- No corpus-wide tag or link reconciliation — that is the future `lint`
  command's job.
- No modification of `file`/`resource-ingestion` behavior; this change exercises
  the existing taxonomy contract rather than altering it.

## Decisions

**Skill-only, no Python CLI.** Retrieval is reading Markdown the agent already
has tools for (Grep/Read over `wiki/`). A Python retriever would add a
dependency and a sync-burden for no gain at this corpus size. *Alternative:* a
`wiki-query` CLI doing keyword/embedding search — rejected as premature; revisit
only if the corpus outgrows index-first reading.

**Index-first retrieval.** The command reads `wiki/index.md` (already a
type-grouped catalog with one-line summaries) to pick candidate pages, then
reads those page bodies — rather than globbing every file. This keeps token cost
bounded and uses the bookkeeping the wiki already maintains. Grep over `wiki/`
is a fallback when the index's summaries are too coarse to locate a page.

**Answer first, file second (and optional).** The command always produces an
answer in conversation; filing is a separate, explicitly-offered step gated on
the user's commit. This preserves the "curator decides what enters the corpus"
principle and avoids polluting `wiki/analyses/` with throwaway lookups.

**`analysis` pages reuse the dual-voice shape.** Like `summary` pages, an
`analysis` page separates the LLM's `## Answer` (neutral, cited synthesis) from
the curator's `## Why this matters`. This keeps the two-voice discipline uniform
across the wiki. The front-matter adds `question:` (the original prompt) and
`sources:` (the cited pages) to the common `type/title/created/tags` set.
*Alternative:* a single free-form body — rejected for breaking the established
voice separation and losing the queryable `question`/`sources` metadata.

**Honesty contract.** The synthesis is restricted to what the cited pages
support. When coverage is partial or absent, the command says so; any
outside-knowledge supplement is labeled and carries no `[[wikilink]]` citation.
This protects the wiki's credibility — a cited claim must trace to a real page.

**Bookkeeping symmetry with `file`.** Filing an analysis updates `index.md`
(under `Analyses`) and appends a `## [<date>] query: <subject>` line to
`log.md`, matching the `ingest:` convention so the log stays greppable by the
`## [` prefix.

## Risks / Trade-offs

- **Hallucinated citations** (a `[[wikilink]]` to a page that doesn't say what
  the answer claims) → the honesty requirement plus a pre-commit validation step
  that every `[[wikilink]]` resolves to a real page filename, mirroring `file`'s
  link check.
- **Index drift** — if `index.md` is stale, retrieval misses pages → fall back
  to Grep over `wiki/` bodies; index maintenance/repair is `lint`'s concern.
- **Scope creep toward search infrastructure** → explicitly a non-goal; the
  design stays skill-only and index-first until the corpus demonstrably needs
  more.
- **Slug collision** with an existing analysis → append `-2`, `-3`, … exactly as
  `file` does for summaries.

## Migration Plan

Additive only. New skill, new template, new spec, and a documented `analysis`
front-matter schema; no existing pages, code, or specs change. `wiki/analyses/`
already exists (with `.gitkeep`). Nothing to roll back beyond deleting the new
files if abandoned.

## Open Questions

- Should a filed `analysis` always add a back-link from each cited hub page, or
  only from hubs it materially extends? (Spec leaves this as "where
  appropriate"; settle during implementation against real examples.)
- Long-term, does `query` warrant a saved-query or re-run mechanism (re-answer
  an old `question:` as the corpus grows)? Out of scope here; note for a future
  change.
