## 1. Repository scaffold and conventions

- [x] 1.1 Create the directory layout: `raw/`, `wiki/summaries/`,
  `wiki/entities/`, `wiki/concepts/`, `wiki/analyses/` (with `.gitkeep` where
  needed)
- [x] 1.2 Create seed `wiki/index.md` (grouped-by-type catalog) and
  `wiki/log.md` (append-only timeline) with header conventions
- [x] 1.3 Write the wiki schema/conventions into `CLAUDE.md`: page taxonomy,
  two-layer model, front-matter fields for each page type, `[[wikilink]]` and
  Obsidian conventions, slug rules
- [x] 1.4 Add page templates for `summary` (with `## Summary` and `## Why this
  matters` sections), `entity`, and `concept` pages

## 2. Converter tooling

- [x] 2.1 Initialize a `uv` project with `pyproject.toml` at the repo root and
  add `docling` and `markitdown` dependencies (Jina Reader is a plain HTTP call,
  no dependency; used keyless against `r.jina.ai`)
- [x] 2.2 Implement content-type detection (fetch headers / inspect path;
  classify as web-html, pdf, or other; content-type takes precedence over
  extension)
- [x] 2.3 Implement the converter router: web → Jina Reader (HTTP GET to
  `r.jina.ai`), PDF → Docling, other → MarkItDown
- [x] 2.4 Write the immutable `raw/<date>-<slug>.md` twin with front-matter
  (`source`, `fetched-at`, `converter`); never overwrite an existing twin
- [x] 2.5 Expose the router as a CLI command the `file` skill can invoke,
  returning the raw twin path and detected type
- [x] 2.6 On conversion failure (unreachable source, unparseable content,
  service unavailable), write nothing and report the reason; no partial twin

## 3. The `file` command (Claude Code skill)

- [x] 3.1 Create the `file` skill/command that takes a URI or local path
- [x] 3.2 Phase 1 (capture): invoke the converter, write the raw twin, perform
  no wiki writes
- [x] 3.3 Phase 2 (author): read the raw twin and propose page type, tags, and
  `[[wikilinks]]` (including any new hub pages to create); present for review
- [x] 3.3a Tag vocabulary: read existing tags (scan `index.md`/front-matter)
  and prefer them; flag any newly-minted tag explicitly for approval
- [x] 3.4 Solicit and capture the user's "Why this matters" commentary during
  the interview
- [x] 3.5 On commit: write `wiki/summaries/<slug>.md` with both voices and the
  `source`/`raw` front-matter links
- [x] 3.6 On commit: create or append the entity/concept hub pages the summary
  touches, using `[[wikilinks]]`
- [x] 3.7 On commit: update `wiki/index.md` (add the page under its type group)
  and append an entry to `wiki/log.md`
- [x] 3.8 Ensure abandoning before commit leaves only the raw twin (no partial
  wiki writes)

## 4. Validation

- [x] 4.1 Validate the change spec with `openspec validate add-resource-ingestion`
- [x] 4.2 Manually ingest one web URL, one PDF, and one non-PDF document;
  confirm correct routing, dual-voice summary, hub updates, and index/log
  entries
  - Routing verified for all three: web→jina (Jane Street post), PDF→docling
    (arXiv 1706.03762), non-PDF→markitdown (local .md). Full Phase 2 authoring
    (dual-voice summary, hub creation, index/log updates) exercised end-to-end
    via the Jane Street web ingest.
- [ ] 4.3 Confirm the result opens correctly in Obsidian with working
  `[[wikilinks]]`
