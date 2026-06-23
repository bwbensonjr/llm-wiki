# llm-wiki — conventions

An LLM-managed knowledge wiki: a local-first git repo of Markdown files. The
human curates sources and asks questions; the LLM summarizes, cross-references,
files, and keeps the books. These conventions are binding for any operation
that reads or writes wiki content.

## Two-layer storage

| Layer   | Mutability | Authored by | Contains                                   |
|---------|------------|-------------|--------------------------------------------|
| `raw/`  | immutable  | converter   | mechanical Markdown twin of each source    |
| `wiki/` | evolving   | LLM + human | summaries, hub pages, `index.md`, `log.md` |

A `raw/` twin, once written, is **never** edited or renamed by a later
operation. All judgment lives in `wiki/`.

## Page taxonomy

Every knowledge page carries a `type` front-matter field, one of:

- `summary` — **source-anchored.** Exactly one per ingested source, written
  once at ingest. The "leaves." Stored in `wiki/summaries/`.
- `entity` — a person, organization, or place. A "hub." `wiki/entities/`.
- `concept` — an abstract idea or topic. A "hub." `wiki/concepts/`.
- `analysis` — a filed-back query answer or comparison. `wiki/analyses/`.
  (Defined now; produced by the future `query` command.)

A `type` outside this set is invalid: halt and report rather than write.

Two bookkeeping files live at `wiki/` root:

- `wiki/index.md` — catalog of every page, grouped by type, each a `[[wikilink]]`
  plus a one-line summary. Updated on every ingest.
- `wiki/log.md` — append-only timeline. One `## [<date>] <op>: <subject>` entry
  per operation; never rewrite existing entries.

Folders mirror `type`. They exist for legibility and to give an unambiguous
"write here" rule — Obsidian resolves links by filename regardless of folder.

## Front-matter

Raw twin — `raw/<date>-<slug>.md`:

```yaml
---
source: <original URL or local path>
fetched-at: <YYYY-MM-DD>
converter: jina | docling | markitdown
---
```

Summary page — `wiki/summaries/<slug>.md`:

```yaml
---
type: summary
title: <Human-readable title>
created: <YYYY-MM-DD>
source: <original URL or local path>
raw: raw/<date>-<slug>.md
tags: [<tag-a>, <tag-b>]
---
```

A summary points both ways: `source:` to the live URL/path, `raw:` to the local
twin. Its body has exactly two named sections: `## Summary` (LLM's neutral
distillation) and `## Why this matters` (the curator's commentary).

Hub page — `wiki/entities/<slug>.md`, `wiki/concepts/<slug>.md`:

```yaml
---
type: entity | concept
title: <...>
created: <YYYY-MM-DD>
tags: [<...>]
---
```

Page templates live in `templates/` (`summary.md`, `entity.md`, `concept.md`).

## Wikilinks & Obsidian

All cross-references use Obsidian-compatible `[[wikilinks]]` that resolve by
page **filename** (the slug), independent of folder. The whole wiki is one git
repo; pages are plain Markdown with YAML front-matter so they open directly in
Obsidian.

## Slugs

Slug = the title slugified: lowercased, ASCII, spaces and punctuation collapsed
to single hyphens. Collisions get a numeric suffix (`-2`, `-3`, …).

- Raw twin (Phase 1): slug from the **source's extracted title** (converter H1 /
  document title), falling back to the URL path segment or local filename. Keeps
  a `<date>-` prefix for chronology and collision resistance.
- Wiki summary (Phase 2): slug from the **final human-readable `title`** settled
  during the interview, no date prefix. This is the canonical slug for links.

## Tags

Prefer tags already in use in the wiki over minting near-duplicates. Surface any
genuinely new tag explicitly for the user to approve. Corpus-wide tag cleanup is
the future `lint` command's job, not ingest's.

## Converter routing (Phase 1)

`file <uri-or-path>` detects content type (fetched content type takes
precedence over extension) and routes:

- web URL (HTML) → Jina Reader (`https://r.jina.ai/<url>`). `r.jina.ai` now
  requires auth; set `JINA_API_KEY` in the environment (sent as a Bearer token).
- PDF (local or URL resolving to PDF) → Docling
- any other file type → MarkItDown

Conversion is all-or-nothing: on any failure, write nothing and report why.

## Python

This repo's converter is a `uv` project (`pyproject.toml` at root). Use `uv`,
not `pip`. Strings use double quotes. The CLI entry point is `wiki-capture`.
