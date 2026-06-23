## Why

The wiki can ingest sources (`file`) but cannot yet be *interrogated*. The
`analysis` page type is defined in the taxonomy — "a filed-back query answer or
comparison" — but nothing produces it: `wiki/analyses/` is empty and there is no
`analysis` template. A curator who has filed a dozen sources has no first-class
way to ask a question across them, get a corpus-grounded answer, and capture
that answer as a durable, cross-linked page. The `query` command closes that
loop and turns the wiki from a write-only archive into a knowledge base.

## What Changes

- Add a `query` command (an LLM skill, `.claude/skills/query/SKILL.md`) that
  takes a natural-language question and answers it **from the wiki corpus**.
- **Retrieve, then synthesize:** the command surveys `wiki/index.md` and reads
  the relevant summary/entity/concept pages, then composes an answer grounded in
  those pages and cited with `[[wikilinks]]` back to them.
- **Honesty about coverage:** when the corpus does not cover the question, the
  command says so plainly rather than answering from outside knowledge, and may
  suggest filing a source first. Outside knowledge, if offered, is clearly
  marked as not corpus-backed.
- **Optional file-back:** after answering, the command offers a propose → coach
  → commit interview to file the answer as an `analysis` page under
  `wiki/analyses/`. A quick lookup need not write anything; the curator decides.
- **Filing an analysis** writes `wiki/analyses/<slug>.md`, links cited pages
  both ways where appropriate, and updates `wiki/index.md` and `wiki/log.md`.
- Add a `templates/analysis.md` page template and define the `analysis`
  front-matter schema (extending the templates and conventions already in
  `CLAUDE.md`).

## Capabilities

### New Capabilities
- `corpus-query`: answering a natural-language question against the wiki corpus
  with cited, corpus-grounded synthesis, and optionally filing the answer back
  as an `analysis` page (with index/log bookkeeping) under a curator-gated
  commit.

### Modified Capabilities
<!-- The `analysis` type and the `wiki/analyses/` folder are already part of the
     page-taxonomy requirement in resource-ingestion; this change exercises that
     contract rather than altering it. No existing requirements change. -->
- _None._

## Impact

- **New skill:** `.claude/skills/query/SKILL.md`.
- **New template:** `templates/analysis.md`.
- **New spec:** `openspec/specs/corpus-query/spec.md` (via this change's delta).
- **Docs:** `CLAUDE.md` gains the `analysis` front-matter schema; `README.md`
  and the command roadmap note `query` as implemented.
- **Wiki content:** `wiki/analyses/` begins to hold pages; `index.md` and
  `log.md` gain `analysis` entries and `query` log lines.
- **No Python CLI changes:** retrieval is LLM-driven over local Markdown, so no
  converter or `wiki_ingest` work is required.
