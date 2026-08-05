# llm-wiki — conventions

An LLM-managed knowledge wiki: a local-first git repo of Markdown files. The
human curates sources and asks questions; the LLM summarizes, cross-references,
files, and keeps the books — and on the unattended path also exercises the
judgment calls (classification, tags, figure selection, drafted significance)
that the curator would otherwise make live. Human judgment is not removed, it is
**moved after the write**: machine-authored pages land as `status: provisional`
and the curator endorses, corrects, or rejects them later via `curate`. Capture
cadence and review cadence are deliberately decoupled. These conventions are
binding for any operation that reads or writes wiki content.

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
  Produced by the `query` command.

A `type` outside this set is invalid: halt and report rather than write.

Every knowledge page also carries a `status` front-matter field, one of:

- `provisional` — machine-authored: written without curator review, by the
  unattended ingest path. Its classification, tags, figure decisions, and
  `## Why this matters` prose are the LLM's judgment, not yet endorsed.
- `reviewed` — curator-endorsed: the curator stands behind the page as written,
  whoever first drafted the prose. Interactive `file` and `query` commits write
  `reviewed` directly, since the curator approved the page at commit time.

A `status` outside this set is invalid: halt and report rather than write. The
review queue is *derived* — the set of pages carrying `status: provisional` —
never a separate maintained list, so it cannot drift from the corpus.

Two bookkeeping files live at `wiki/` root:

- `wiki/index.md` — catalog of every page, grouped by type, each a `[[wikilink]]`
  plus a one-line summary. Updated on every ingest.
- `wiki/log.md` — append-only timeline. One `## [<date>] <op>: <subject>` entry
  per operation; never rewrite existing entries. The `<op>` vocabulary is
  `ingest` (a filed source — an unattended one says so in its body), `query` (a
  filed-back analysis), `lint` (a repair run), and `curate` (a review run: what
  was endorsed, merged, and rejected, with rejection reasons).

**Wikilinks in `log.md`.** Because the log is append-only and the corpus is not, a
`[[wikilink]]` in a log entry can be un-made by a later operation that the log is
forbidden to go back and repair. Two rules follow:

- **Name a page in plain text when the entry is recording its removal** — the page
  rejected by a `curate` run, or the variant folded away by a merge. Its slug in
  backticks, plus the source URL for a rejection. A link written to a page you are
  deleting in the same breath is born broken, and it is the one case the writer can
  always see coming. Elsewhere in the log, link normally: most pages persist, and
  clickable history is worth having.
- **An unresolvable wikilink in `log.md` is not a `lint` defect.** The log records
  what was true when the entry was written. `lint` must skip `log.md` in its
  broken-link check rather than report a defect that no operation is permitted to
  fix — the same reasoning that keeps `status: provisional` off the defect list.

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
status: provisional | reviewed
title: <Human-readable title>
created: <YYYY-MM-DD>
source: <original URL or local path>
raw: raw/<date>-<slug>.md
tags: [<tag-a>, <tag-b>]
---
```

A summary points both ways: `source:` to the live URL/path, `raw:` to the local
twin. Its body has exactly two named sections: `## Summary` (LLM's neutral
distillation) and `## Why this matters` (the resource's significance to the
curator).

`## Why this matters` is **endorsement-gated, not authorship-gated.** On the
interactive path the curator supplies it in their own words and the page commits
as `reviewed`. On the unattended path the LLM drafts it — seeded by the
`inbox.md` curator note when one was given — and the page commits as
`provisional`. `status: reviewed` means the curator stands behind the stated
significance regardless of who first drafted the prose. The `status` field is the
**sole** marker of that distinction: the body carries no inline authorship
disclaimer, so endorsement is a one-field edit and no stale disclaimer can
survive review.

Hub page — `wiki/entities/<slug>.md`, `wiki/concepts/<slug>.md`:

```yaml
---
type: entity | concept
status: provisional | reviewed
title: <...>
created: <YYYY-MM-DD>
tags: [<...>]
---
```

Analysis page — `wiki/analyses/<slug>.md`:

```yaml
---
type: analysis
status: provisional | reviewed
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
commentary, under the same endorsement rule as a summary's). Every cited claim
must trace to a real page; outside knowledge, if included, is marked as not
corpus-backed.

Page templates live in `templates/` (`summary.md`, `entity.md`, `concept.md`,
`analysis.md`).

## The inbox queue (`inbox.md`)

`inbox.md` at the **repo root** is the queue of sources awaiting unattended
ingest. Each entry is one Markdown checklist line — a URL or local path, plus an
optional separator and free-text curator note. The checkbox carries the state:
`- [ ]` unprocessed, `- [x]` ingested, `- [!]` parked after a failure with a
dated reason. The unattended path updates checkboxes in place and **never deletes
an entry**, which is what makes re-runs idempotent and keeps the file a legible
record of what was queued.

The curator note is the only genuine curator voice available at unattended ingest
time; when present it seeds that page's drafted `## Why this matters`.

It lives at the root, **not** under `wiki/`, on purpose: it is not a knowledge
page, so Quartz must not publish it and `lint` must not read it as a page missing
a `type`. It is committed rather than gitignored so the curator can append to it
from another machine.

**There is no per-run batch cap** — deliberately. The queue's length is the
curator's throttle, and a cap would only hide review debt that `curate`'s
queue-size report is meant to make visible. Revisit only if unbounded runs prove
to be a problem in practice.

## `lint` vs `curate`

Two housekeeping commands, deliberately orthogonal — do not fold either into the
other:

- **`lint` audits structure.** Invalid front-matter, `type`/folder mismatches,
  broken wikilinks, orphans, index/log drift, missing sections, near-duplicate
  tags. It *repairs*. A clean corpus reports no defects — which is why a
  `status: provisional` page is **not** a lint defect: treating it as one would
  make an auto-ingesting wiki permanently "dirty" and destroy the clean/dirty
  signal that makes `lint` worth running.
- **`curate` exercises judgment.** It reviews the provisional queue and
  *endorses, retags, reclassifies, merges, and rejects*. Rejection deletes a page;
  that is not a repair. `curate` reuses `lint`'s shape (read-only survey,
  propose → coach → commit, one appended log entry) without inheriting its
  contract, and never repairs a structural defect it happens to notice.

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
- Wiki summary (Phase 2): slug from the **final human-readable `title`** — settled
  during the interview on the interactive path, chosen by the LLM on the
  unattended one — with no date prefix. This is the canonical slug for links.

## Tags

Prefer tags already in use in the wiki over minting near-duplicates. A genuinely
new tag is never minted silently — but *when* it is approved depends on the path:

- **Interactive** (`file`, `query`): surface every new tag explicitly for the
  user to approve or redirect **before commit**.
- **Unattended** (`ingest-inbox`): there is no approver present, so approval is
  **deferred, not skipped**. The tag may be committed, but the page carries
  `status: provisional` and that ingest's `wiki/log.md` entry names every tag the
  run minted, so the new vocabulary is visible at review and `curate` can approve
  it or redirect it via the retag verb.

Corpus-wide tag cleanup (near-duplicate and orphan tags across the whole corpus)
is the `lint` command's job, not ingest's.

## Converter routing (Phase 1)

Capture is identical on both paths — `file <uri-or-path>` and `ingest-inbox` both
shell out to the same `wiki-capture` CLI, which detects content type (fetched
content type takes precedence over extension) and routes:

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

A figure's *knowledge* reaches `wiki/` as **prose**. On the **interactive** path
the Phase 2 interview is the review/consent point — the LLM presents the localized
figures, distills the meaningful ones into `## Summary`, and the user drops any
noise. On the **unattended** path there is no interview, so that judgment is the
LLM's: it decides which figures carry meaning, distills those, and drops the rest.
A dropped figure is not distilled or promoted; its `raw/assets/` bytes remain. Those
surviving bytes are **not** a defect — dropping is the common case, so a raw asset
that never reached `wiki/` is the design working, not drift. What `lint` checks is
that the twin↔assets correspondence holds: no `raw/assets/<stem>/` without its
`raw/<stem>.md`, no asset file its own twin does not link to, no twin link pointing
at an asset that is not there. Because `raw/` is immutable, those findings are
**reported and never repaired**. A figure's *bytes* reach the
published site only by **lazy promotion** — when a figure must be seen (prose
cannot carry it) and either the user approves or, unattended, the LLM so judges, a
curated copy moves into `wiki/assets/` (created on first use) and is embedded in
the summary as `![[<filename>]]`; the `raw/assets/` original stays the source of
truth. That leading `!` makes it a distinct link class: an **embed resolves against
`wiki/assets/`**, not against page slugs, so it is checked against the files there
and never against the page set. Unattended
figure decisions — which figures were distilled, which were promoted — are recorded
in that ingest's `wiki/log.md` entry, so they are visible at review and reversible:
`curate` deletes a promoted copy from `wiki/assets/` when the page is rejected or
the figure revised away, leaving the `raw/assets/` original in place.
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
- **Provisional pages publish, unfiltered.** This is an information source, not
  an operational system needing staged release, so nothing gates a
  `status: provisional` page from going live. **Open follow-up:** `status` is
  therefore currently visible only in the repo — Quartz v4 does not render
  arbitrary front-matter, so a site reader cannot yet distinguish a
  machine-judged page from an endorsed one. Options considered: a small Quartz
  component, or a `provisional` tag riding along in `tags:` (visible and
  filterable, but duplicates state that already lives in `status`). Deferred; it
  does not block the queue mechanics.
