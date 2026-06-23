## 1. Define the analysis page contract

- [x] 1.1 Add `templates/analysis.md` with `analysis` front-matter (`type`,
  `title`, `created`, `source` question, `tags`, `sources`) and a body of
  exactly `## Answer` and `## Why this matters`, mirroring `templates/summary.md`
- [x] 1.2 Document the `analysis` front-matter schema in `CLAUDE.md` under
  Front-matter, including the `question:` and `sources:` fields and the
  two-section body
- [x] 1.3 Add `templates/analysis.md` to the templates list noted in `CLAUDE.md`

## 2. Author the query skill

- [x] 2.1 Create `.claude/skills/query/SKILL.md` with name `query` and a
  description matching the `file` skill's style (so the harness surfaces it)
- [x] 2.2 Write the retrieval step: read `wiki/index.md` to pick candidate
  pages, read their bodies, fall back to Grep over `wiki/` when index summaries
  are too coarse
- [x] 2.3 Write the synthesis step: compose a corpus-grounded answer with inline
  `[[wikilink]]` citations to the pages used
- [x] 2.4 Write the honesty contract: state when the corpus does not cover the
  question; mark any outside-knowledge supplement as not corpus-backed with no
  false citation; optionally suggest filing a source
- [x] 2.5 Write the optional file-back interview (propose → coach → commit):
  default to writing nothing; propose type/title/tags/links/answer; solicit the
  curator's "Why this matters"; prefer existing tags and flag new ones
- [x] 2.6 Write the commit step: write `wiki/analyses/<slug>.md` from the
  template (slug from final title, `-2`/`-3` on collision), add back-links from
  cited hubs where appropriate, update `wiki/index.md` under `Analyses`, append
  a `## [<date>] query: <subject>` entry to `wiki/log.md`
- [x] 2.7 Write the pre-commit validation: `type` is `analysis`, both voices
  present, every `[[wikilink]]` resolves to a real page filename and is unbroken
  by line wrapping; halt and report on any invalid `type`
- [x] 2.8 Add a Guardrails section (answer writes nothing until commit;
  index/log bookkeeping required; no fabricated citations)

## 3. Documentation

- [x] 3.1 Update `README.md` to describe the `query` command alongside `file`
- [x] 3.2 Update the command roadmap note (memory/roadmap) so `query` is marked
  done and only `lint` remains planned

## 4. Verify end-to-end

- [x] 4.1 Run a query the corpus covers; confirm a cited, corpus-grounded answer
  and that no files change when filing is declined
- [x] 4.2 Run a query the corpus does not cover; confirm the command says so
  instead of fabricating citations
- [x] 4.3 File one answer as an `analysis` page; confirm front-matter, both
  voices, valid wikilinks, and that `index.md` and `log.md` were updated
- [x] 4.4 Open the resulting `analysis` page in Obsidian (or verify link syntax)
  to confirm wikilinks resolve
