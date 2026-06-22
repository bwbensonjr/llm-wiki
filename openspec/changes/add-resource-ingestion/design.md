# Design: Resource Ingestion

## Context

The wiki is a local-first git repository of Markdown files. The human curates
sources (usually by URI, sometimes by local file path) and the LLM does the
filing. This design fixes the structure and the ingest flow that all later
operations depend on. It follows Karpathy's llm-wiki classification rather than
an actionability spine like PARA — the organizing axis is *what a thing is
about*, not *how soon it is needed*.

## Repository layout

```
llm-wiki/
  raw/                  immutable Markdown twins of ingested sources
    2026-06-22-<slug>.md
  wiki/
    summaries/          one page per ingested source (the "leaves")
    entities/           people, orgs, places (the "hubs")
    concepts/           abstract ideas (the "hubs")
    analyses/           filed-back query answers, comparisons
    index.md            catalog of every wiki page
    log.md              append-only timeline of ingests/queries/lints
```

Folders mirror the `type` field. Obsidian resolves `[[wikilinks]]` by filename
regardless of folder, so the folders exist for human/LLM legibility and to give
the `file` command an unambiguous "write here" rule — not for link resolution.

## Two families of page

Page types split by their relationship to sources:

- **Source-anchored** — `summary` pages. Exactly one per ingested source,
  written once at ingest. The "leaves."
- **Synthesis** — `entity`, `concept`, `analysis` pages. Each aggregates across
  many sources and grows over time as new summaries link into it. The "hubs."

Ingest writes a leaf, then enriches the hubs that leaf touches. This is the
engine of the wiki.

## Storage layers and their link

| Layer  | Mutability | Authored by  | Contains                                   |
|--------|------------|--------------|--------------------------------------------|
| `raw/` | immutable  | converter    | mechanical Markdown twin of the source     |
| `wiki/`| evolving   | LLM + human  | summaries, hubs, index, log                |

A summary page points both ways: `source:` to the live URL/path and `raw:` to
the local twin. The twin is link-rot insurance and a stable thing to re-read;
the wiki page is where all judgment lives.

## Converter router

One ingest entry point, routed by content type:

```
file <uri-or-path>
  ├─ web URL              → Jina Reader (https://r.jina.ai/<url>)
  ├─ PDF                  → Docling
  └─ other file types     → MarkItDown
       (docx, pptx, xlsx, images, media, …)
```

Rationale:
- **Jina Reader** for web because its extracted Markdown is clean and the cost
  (sending a URL to a third party) only applies to already-public URLs.
- **Docling** for PDFs because of its superior layout/table fidelity on papers
  and documents.
- **MarkItDown** as the generalist for the long tail of office and media
  formats.

All three are invoked locally via `uv`-managed tooling except Jina Reader, which
is a hosted HTTP call. Local files never leave the machine.

### Decisions

- **Jina Reader is hosted, not self-hosted (for now).** Simplicity over
  zero-external-calls. Self-hosting is a documented future option, not in scope.
- **Jina Reader is used keyless** against `r.jina.ai` to start, accepting its
  rate limits. If limits become a problem we add an API key later; not in scope
  now.
- **Routing is by detected content type, not file extension alone.** A URL that
  resolves to a PDF should still go to Docling; detection should consider the
  fetched content type, falling back to extension.

### Failure handling

Conversion is all-or-nothing. If Phase 1 fails for any reason — source
unreachable, converter cannot parse it, or the routed service is unavailable —
the command writes nothing (no `raw/` twin, no `wiki/` pages) and reports the
reason. There is no partial-twin state to clean up.

### Tooling layout

The converter is a standard `uv` project with `pyproject.toml` at the repo root.
`docling` and `markitdown` are project dependencies; Jina Reader is a plain HTTP
call (no dependency).

## The two-phase `file` command

```
PHASE 1 — capture (mechanical, no judgment)
  detect type → route to converter → write raw/<date>-<slug>.md
  raw front-matter: source, fetched-at, converter
  (safe to abandon here: leaves only a harmless raw twin, no wiki writes)

PHASE 2 — author (interview: propose → coach → commit)
  LLM reads the raw twin and proposes:
    • page type (summary, usually)
    • tags
    • [[wikilinks]] to existing entity/concept pages
    • any NEW entity/concept hub pages to create
    • a draft summary
  Human reviews and coaches (re-tag, re-link, fold an entity into another, …).
  On "file it", LLM writes:
    • wiki/summaries/<slug>.md  (two voices, see below)
    • updates to each entity/concept hub it touches (create or append)
    • a new line in index.md
    • an appended entry in log.md
```

The human's "why I find this interesting" commentary is collected during the
interview and stored on the summary page, distinct from the LLM's neutral
distillation. This dual-voice page is a deliberate addition to Karpathy's
design, which has no slot for the curator's opinion.

## Front-matter schema

Raw twin (`raw/<date>-<slug>.md`):

```yaml
---
source: https://example.com/article    # original URL or local path
fetched-at: 2026-06-22
converter: jina | docling | markitdown
---
```

Wiki summary page (`wiki/summaries/<slug>.md`):

```yaml
---
type: summary
title: Human-readable title
created: 2026-06-22
source: https://example.com/article
raw: raw/2026-06-22-<slug>.md
tags: [tag-a, tag-b]
---
```

Hub page (`wiki/entities/<slug>.md`, `wiki/concepts/<slug>.md`):

```yaml
---
type: entity | concept
title: ...
created: 2026-06-22
tags: [...]
---
```

Summary page body has two named sections — `## Summary` (LLM distillation) and
`## Why this matters` (human commentary) — plus inline `[[wikilinks]]`.

## Tag vocabulary

Tags are curation signal and only stay useful if they converge rather than
fragment (`eval` vs. `evaluation` vs. `benchmarks` for one idea). To keep the
vocabulary tight at the point of entry:

- Before proposing tags in Phase 2, the LLM reads the tags already in use
  (e.g. by scanning `index.md` or front-matter) and prefers existing tags.
- Any genuinely new tag the LLM wants to mint is surfaced explicitly during the
  interview, so the user approves or redirects it (turning a one-time coaching
  correction into a durable convention).

This is *prevention* at ingest time — one page at a time. Corpus-wide tag
reconciliation (finding and merging near-duplicate or orphan tags that already
exist across the whole wiki) is a *cure* and belongs to the future `lint`
command, not this change.

## index.md and log.md

- `index.md` is a catalog: every wiki page listed with a link and a one-line
  summary, grouped by type. Updated on every ingest. Lets the LLM navigate
  without embeddings.
- `log.md` is append-only: one entry per operation (ingest now; query/lint
  later), greppable via a stable `## [` heading pattern.

## Slug derivation

Slugs derive from the **page title**, slugified: lowercased, ASCII, spaces and
punctuation collapsed to single hyphens. There is a sequencing wrinkle because
the two layers learn the title at different times:

- **Raw twin (Phase 1)** — the wiki title is not chosen until the Phase 2
  interview, so the twin's slug is derived from the *source's own extracted
  title* (the converter's H1 / document title metadata), falling back to the URL
  path segment or local filename when no title is extractable. The twin keeps a
  `<date>-` prefix (`raw/2026-06-22-<slug>.md`) for chronology and collision
  resistance.
- **Wiki summary (Phase 2)** — the slug derives from the final human-readable
  `title` settled during the interview (`wiki/summaries/<slug>.md`, no date
  prefix).

Collisions are resolved by appending a numeric suffix (`-2`, `-3`, …). A raw
twin once written is never renamed (it is immutable); the wiki page slug is the
canonical one for `[[wikilinks]]`.

## Open questions

- Whether `analysis` pages live under `wiki/analyses/` from day one or are
  deferred until the `query` command exists (they are produced by query). They
  are defined in the taxonomy now but may have no producer until then.
