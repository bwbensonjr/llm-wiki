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

Analysis page — `wiki/analyses/<slug>.md`:

```yaml
---
type: analysis
title: <Human-readable title>
created: <YYYY-MM-DD>
question: <the original question, verbatim>
tags: [<tag-a>, <tag-b>]
sources: ["[[<cited-page>]]", "[[<cited-page>]]"]
---
```

The `sources:` value is a YAML list of quoted `[[wikilink]]` strings. The quotes
are required: bare `[[...]]` is invalid YAML and breaks strict parsers (e.g. the
publish pipeline), even though Obsidian tolerates it. Obsidian still renders the
quoted wikilinks as links in the property.

An analysis is a filed-back `query` answer. `question:` records the prompt that
produced it and `sources:` lists the wiki pages it cites. Like a summary, its
body has exactly two named sections: `## Answer` (the LLM's corpus-grounded
synthesis, with inline `[[wikilinks]]`) and `## Why this matters` (the curator's
commentary). Every cited claim must trace to a real page; outside knowledge, if
included, is marked as not corpus-backed.

Page templates live in `templates/` (`summary.md`, `entity.md`, `concept.md`,
`analysis.md`).

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

## Image handling

Image localization is **default-on and scoped to the web/Jina route.** For a web
page, Phase 1 automatically:

- downloads that source's **content** images into `raw/assets/<twin-stem>/` —
  immutable raw bytes, the source of truth, keyed to the twin's filename stem;
- rewrites the twin's image links to those local relative paths (done before the
  single twin write, so the immutable twin is never edited after the fact);
- skips avatars/thumbnails/undersized images mechanically (no LLM judgment), and
  tolerates a single image's download failure by leaving its link remote.

The mechanical filter is the selectivity control, so a text-dominant page yields
no content images and downloads nothing. Pass `--no-images` to `wiki-capture` to
suppress localization entirely for the rare page whose figures are worthless.

A figure's *knowledge* reaches `wiki/` as **prose**: the Phase 2 interview is the
review/consent point — the LLM presents the localized figures, distills the
meaningful ones into `## Summary`, and the user drops any noise (a dropped figure
is not distilled or promoted; its `raw/assets/` bytes remain, and unreferenced
raw assets are a future `lint` concern). A figure's *bytes* reach the published
site only by **lazy promotion** — when a figure must be seen and the user
approves, a curated copy moves into `wiki/assets/` (created on first use) and is
embedded in the summary; the `raw/assets/` original stays the source of truth.
Both `raw/assets/` and `wiki/assets/` are content and are committed — they are not
in `.gitignore`.

## Python

This repo's converter is a `uv` project (`pyproject.toml` at root). Use `uv`,
not `pip`. Strings use double quotes. The CLI entry point is `wiki-capture`.

## Toolchain (mise)

Tooling is managed by [mise](https://mise.jdx.dev). `mise.toml` (committed) pins
what the project needs — `python`, `uv`, `node`, and the **openspec** CLI
(`npm:@fission-ai/openspec`). mise auto-activates per directory, so once it's
installed, `cd`-ing into the repo puts the right tools on `PATH`. Run mise-only
tools explicitly when needed, e.g. `mise exec -- openspec validate <change>`.

**Secrets never go in `mise.toml`.** `JINA_API_KEY` (used by the Jina Reader
route) belongs in `mise.local.toml`, which is gitignored:

```toml
# mise.local.toml  (do NOT commit)
[env]
JINA_API_KEY = "jina_..."
```

mise merges `mise.local.toml` over `mise.toml`, so the key is on your
environment without ever entering git history.

## Version control & `.gitignore`

Commit content and code; never commit generated, machine-local, or
session-local state. The current `.gitignore` covers:

- **Editor/OS cruft** — `*~`, `.DS_Store`.
- **Python build artifacts** — `__pycache__/`, `*.py[cod]`, and the `.venv/`
  virtualenv. These are regenerated by `uv`; the lockfile `uv.lock` *is*
  tracked (it pins dependencies), but the resolved environment is not.
- **Obsidian local config** — the whole `.obsidian/` vault folder. It is
  auto-created when the vault is opened and is dominated by `workspace.json`,
  which stores per-machine UI state (pane layout, panel widths, last-open
  files) that churns every session and conflicts on merge. It is not content
  and Obsidian regenerates it from defaults, so it stays on disk but untracked.
- **Local mise overrides** — `mise.local.toml`, which holds machine-local
  config and secrets (e.g. `JINA_API_KEY`). The committed `mise.toml` stays
  secret-free.
- **Publish pipeline artifacts** — `public/` (built site), `.quartz/` (the
  pinned Quartz checkout cloned at build time), and `node_modules/`. All are
  regenerated by `scripts/build-site.sh` and never committed.

Rule of thumb: if a file is rebuilt automatically or differs per machine, it
belongs in `.gitignore`, not the repo. When staging, prefer explicit paths over
`git add -A` so regenerated state is not swept in by accident.

## Publishing

The curated `wiki/` layer is published as a static HTML site with
[Quartz](https://quartz.jzhao.xyz) and hosted on GitHub Pages. Publishing is
read-only over `wiki/`; it never reads or alters `raw/`.

- **Renderer** — Quartz v4, pinned in `scripts/build-site.sh`. Quartz is a
  project scaffold, not an npm library, so the script clones the pinned version
  into `.quartz/` (gitignored), overlays the repo-root `quartz.config.ts`, and
  builds with `npx quartz build --directory wiki --output public`. Content is
  read in place; pointing `--directory` at `wiki/` is what structurally excludes
  the `raw/` twins.
- **Config** — `quartz.config.ts` lives at the repo root and is the only Quartz
  customization surface. Its `./quartz/...` imports resolve only after the file
  is copied into `.quartz/`, so an unresolved-import warning in the repo is
  expected. Keep customization minimal (title, `baseUrl`); wikilink resolution
  relies on `CrawlLinks({ markdownLinkResolution: "shortest" })`.
- **Deploy** — `.github/workflows/publish.yml` builds and deploys to GitHub
  Pages on push to `main` and on `workflow_dispatch`. Enabling Pages (Settings →
  Pages → Source = GitHub Actions) is a one-time manual maintainer step.
- **Front-matter must be valid YAML** — Quartz uses a strict YAML parser. Bare
  `[[wikilinks]]` in front-matter values (e.g. the analysis `sources:` field)
  break it even though Obsidian tolerates them; quote them as a YAML list:
  `sources: ["[[a]]", "[[b]]"]`.
