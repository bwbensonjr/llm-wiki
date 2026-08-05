---
name: file
description: File a resource into the llm-wiki. Converts a URL or local file into an immutable raw twin, then runs a propose→coach→commit interview to author a dual-voice summary page and update the entity/concept hubs, index, and log. Use when the user wants to ingest, file, capture, or add a source to the wiki.
metadata:
  author: llm-wiki
  version: "1.0"
---

# The `file` command

File a resource (a URL or a local path) into the wiki. Run the two phases in
order. **Phase 1 is mechanical; Phase 2 is an interview — never skip the review
or the commit gate.** Read the repo `CLAUDE.md` for the page taxonomy,
front-matter schema, slug rules, and tag conventions; they are binding here.

**Input:** the resource to file is given as an argument (a URL or local path).
If none was provided, ask the user for it before doing anything.

---

## Phase 1 — capture (mechanical, no judgment)

Run the converter CLI from the repo root:

```bash
uv run wiki-capture "<uri-or-path>"
```

This detects the content type, routes it (web→Jina Reader, PDF→Docling,
other→MarkItDown), and writes the immutable twin `raw/<date>-<slug>.md`.

**Images localize automatically.** For a web page, capture downloads the
source's **content** images into `raw/assets/<twin-stem>/`, rewrites the twin's
links to the local copies, and skips avatars/thumbnails/tiny images
mechanically — no flag needed. A text page yields no content images and
downloads nothing, so the default is safe. You review what was grabbed in Phase
2 (see below). Only suppress it with `--no-images` in the rare case a page's
figures are worthless and you want to skip the download entirely:

```bash
uv run wiki-capture "<uri-or-path>" --no-images
```

The web/Jina route is the only one affected; PDFs and other files ignore this.

- **On success** it prints a JSON object to stdout:
  `{"raw_path": ..., "converter": ..., "detected_type": ..., "title": ...,
  "images": ...}` (`images` — a `kept`/`skipped` report — present whenever
  localization ran). Parse it and keep `raw_path`.
- **On failure** it prints a JSON `{"error": ...}` to stderr and exits non-zero,
  having written nothing. **Stop here** and report the failure reason to the
  user. Do not write any `wiki/` files.

Do **no** `wiki/` writes in this phase. If the user abandons after Phase 1, the
only artifact is the harmless raw twin — which is correct.

---

## Phase 2 — author (propose → coach → commit)

### 1. Read and propose

Read the raw twin at `raw_path`. **If images were localized** (the twin has
links into `raw/assets/<twin-stem>/`, and the capture JSON listed them under
`images.kept`), this is the review-and-consent step for them: `Read` those
localized figures, then present them to the user and fold the **meaningful** ones
into your draft `## Summary` as prose — describe or transcribe what a figure
shows, since the wiki layer is a distillation, not a copy. Let the user **drop**
any that are noise; a dropped figure is simply not distilled and not promoted —
its `raw/assets/` bytes stay in place (immutable), and unreferenced raw assets
are a future `lint` concern, not this command's. The figure's *knowledge* belongs
in the summary text; its bytes stay in `raw/assets/`.

Then survey the existing wiki so your proposal fits the corpus:

- `wiki/index.md` and existing hub pages under `wiki/entities/` and
  `wiki/concepts/` — to find pages your `[[wikilinks]]` should point to.
- Tags already in use (scan `wiki/index.md` and summary front-matter) — **prefer
  existing tags** over minting near-duplicates.

Present a proposal to the user containing:

- **Page type** — almost always `summary` for an ingested source.
- **Title** — the human-readable title (the wiki slug derives from it).
- **Tags** — drawn from existing tags where they apply. **Flag every genuinely
  new tag explicitly** ("new tag: …") so the user can approve or redirect it.
- **Wikilinks** — `[[links]]` to existing entity/concept pages, plus a list of
  any **new** hub pages you propose to create.
- **Draft `## Summary`** — your neutral distillation of the source.

**Corpus independence applies to everything you draft** (see *Corpus independence* in
`CLAUDE.md`) — a page's conformance must not depend on which path wrote it. You have
just surveyed the corpus, so what you learned about *what is missing* is fresh and
tempting to write down; keep it out of the page. Ask of any sentence mentioning the
wiki: **"would ingesting another source make this false?"** If yes, say what is true of
the subject and stop. So no "X is not an ingested source", no "no page here covers Y",
no "the corpus's only/first/clearest Z", no counting the pages that mention something.
Sibling orientation — situating the subject among related pages the wiki already holds —
is permitted and worth doing. A superlative about *the source* ("the paper's only
measurement of compile-time cost") is also fine; only corpus-scoped ones are banned.

### 2. Coach

Let the user revise anything: re-title, re-tag, re-link, fold one proposed
entity into another, drop a hub, etc. Iterate until they are satisfied.

**Solicit the "Why this matters" commentary.** If the user has not already said
why this resource is interesting, ask them — in their own words. This becomes
the `## Why this matters` section and must be the user's voice, not yours. Do
not commit a summary without it.

If what the user says frames significance as a corpus-membership claim ("nothing else
here covers this", "this is the first page on it"), say so and offer the
corpus-independent rephrasing — the claim goes false on the next ingest, and this
section is where that habit is most natural. Their voice, their call; you raise it
once. If they want the observation kept, it belongs in the `wiki/log.md` entry for this
ingest, which is exempt, not in the page.

### 3. Commit

Only after the user says to file it, write all of the following. (Use the
templates in `templates/` as the starting shape.)

1. **`wiki/summaries/<slug>.md`** — `<slug>` from the final title. Front-matter
   per `CLAUDE.md`: `type: summary`, `title`, `created` (today), `source` (the
   original URL/path from the raw twin), `raw: <raw_path>`, `tags`. Body has
   exactly two sections: `## Summary` (your distillation, with inline
   `[[wikilinks]]`) and `## Why this matters` (the user's commentary). If the
   slug collides with an existing page, append `-2`, `-3`, …

2. **Entity/concept hub pages** the summary touches — for each, either create it
   (`wiki/entities/<slug>.md` or `wiki/concepts/<slug>.md`, from the template)
   or append to the existing page, adding a `[[wikilink]]` back to this summary
   under its Sources. Never duplicate an existing hub.

3. **`wiki/index.md`** — add the new page(s) under the matching type grouping as
   a `[[wikilink]]` plus a one-line summary.

4. **`wiki/log.md`** — append one entry (do not rewrite existing ones):
   `## [<date>] ingest: <title>` followed by a line noting the source and the
   converter used.

**Optional — display a figure on the site.** Prose is the default; only when a
localized figure *must be seen* (a diagram prose cannot replace) and the user
approves, promote it: copy that one file from `raw/assets/<twin-stem>/` into
`wiki/assets/` (create the directory on first use), and embed it in the summary
with an Obsidian image link (`![[<filename>]]` or `![alt](../assets/<filename>)`).
Leave the `raw/assets/` original untouched — it remains the source of truth.
Promote only what needs showing; do not bulk-copy the source's images.

Validate before finishing: the summary's `type` is one of the allowed values,
both voices are present, and every `[[wikilink]]` points to a real or
just-created page filename. Keep each `[[wikilink]]` on a single line —
Obsidian does not resolve a link split across a line break, so never let line
wrapping break one. If anything is off, fix it rather than committing a broken
page.

---

## Guardrails

- Phase 1 writes only the raw twin; never touch `wiki/` until the user commits.
- A `type` outside `summary|entity|concept|analysis` is invalid — halt and
  report instead of writing.
- Raw twins are immutable: never edit or rename a file under `raw/`.
- No corpus-membership claim in a page: no presence/absence claim, no corpus-scoped
  superlative or count. Sibling orientation stays; a noticed gap goes in the log entry.
- If conversion fails, write nothing and tell the user why.
