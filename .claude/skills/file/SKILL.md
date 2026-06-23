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

- **On success** it prints a JSON object to stdout:
  `{"raw_path": ..., "converter": ..., "detected_type": ..., "title": ...}`.
  Parse it and keep `raw_path`.
- **On failure** it prints a JSON `{"error": ...}` to stderr and exits non-zero,
  having written nothing. **Stop here** and report the failure reason to the
  user. Do not write any `wiki/` files.

Do **no** `wiki/` writes in this phase. If the user abandons after Phase 1, the
only artifact is the harmless raw twin — which is correct.

---

## Phase 2 — author (propose → coach → commit)

### 1. Read and propose

Read the raw twin at `raw_path`. Then survey the existing wiki so your proposal
fits the corpus:

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

### 2. Coach

Let the user revise anything: re-title, re-tag, re-link, fold one proposed
entity into another, drop a hub, etc. Iterate until they are satisfied.

**Solicit the "Why this matters" commentary.** If the user has not already said
why this resource is interesting, ask them — in their own words. This becomes
the `## Why this matters` section and must be the user's voice, not yours. Do
not commit a summary without it.

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

Validate before finishing: the summary's `type` is one of the allowed values,
both voices are present, and every `[[wikilink]]` points to a real or
just-created page filename. If anything is off, fix it rather than committing a
broken page.

---

## Guardrails

- Phase 1 writes only the raw twin; never touch `wiki/` until the user commits.
- A `type` outside `summary|entity|concept|analysis` is invalid — halt and
  report instead of writing.
- Raw twins are immutable: never edit or rename a file under `raw/`.
- If conversion fails, write nothing and tell the user why.
