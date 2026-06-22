# Add Resource Ingestion

## Why

This project builds an LLM-managed knowledge wiki in the spirit of Karpathy's
llm-wiki: a local-first git repository of Markdown files where the human curates
sources and asks questions, and the LLM does the grunt work of summarizing,
cross-referencing, filing, and bookkeeping.

Before any of that is possible, the wiki needs (1) a defined structure — what
kinds of pages exist and where they live — and (2) the foundational `file`
command that gets a resource into the wiki. Everything else (query, lint) builds
on the pages this command produces.

This change establishes that foundation: the page taxonomy, the two-layer
storage model, the converter router, and the two-phase interactive `file`
command.

## What Changes

- **Page taxonomy** following Karpathy's classification. Knowledge pages carry a
  `type` of `summary`, `entity`, `concept`, or `analysis`. Two bookkeeping files
  exist: `index.md` (catalog) and `log.md` (append-only timeline).
- **Two-layer storage.** An immutable `raw/` layer holds a Markdown "twin" of
  each ingested source. An authored `wiki/` layer holds the LLM- and
  human-authored pages. The two layers are linked by front-matter.
- **Converter router.** A single ingest path detects content type and routes:
  web URLs → Jina Reader, PDFs → Docling, all other file types → MarkItDown.
- **The `file` command**, run in two phases:
  - *Phase 1 — capture:* mechanically convert the source and write the
    immutable `raw/` twin. No judgment, no wiki writes.
  - *Phase 2 — author:* a propose→coach→commit interview. The LLM proposes a
    page type, tags, and `[[wikilinks]]`; the human reviews and coaches; on
    commit the LLM writes the wiki summary page (carrying two voices — the LLM's
    neutral distillation and the human's "Why this matters" commentary), updates
    the entity/concept hub pages it touches, and updates `index.md` and
    `log.md`.
- **Format & compatibility.** All pages are Markdown with YAML front-matter and
  use Obsidian-compatible `[[wikilinks]]`. The whole wiki is one git repo.

## Capabilities

- resource-ingestion

## Non-Goals

- The `query` command (searching/synthesizing across pages). Future change.
- The `lint` command (contradictions, stale claims, orphan pages). Future change.
- Self-hosting Jina Reader, or any zero-external-call mode. Future option.
- Embeddings, vector search, or any non-grep retrieval infrastructure.
- Multi-user/real-time collaboration beyond what git provides for free.
