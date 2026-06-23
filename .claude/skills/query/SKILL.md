---
name: query
description: Answer a question against the llm-wiki corpus. Surveys the index, reads the relevant summary/entity/concept pages, and synthesizes a cited, corpus-grounded answer — then optionally runs a propose→coach→commit interview to file the answer as an analysis page and update the index and log. Use when the user wants to ask, query, or interrogate the wiki, or compare what its sources say.
metadata:
  author: llm-wiki
  version: "1.0"
---

# The `query` command

Answer a natural-language question **from the wiki corpus**, then optionally file
the answer back as an `analysis` page. Read the repo `CLAUDE.md` for the page
taxonomy, the `analysis` front-matter schema, slug rules, and tag conventions;
they are binding here.

**Input:** the question is given as an argument. If none was provided, ask the
user what they want to know before doing anything.

**The command always answers in conversation first. Filing is a separate,
optional step that writes nothing to the wiki until the user commits.**

---

## Phase 1 — answer (retrieve → synthesize, no wiki writes)

### 1. Retrieve

Find the pages that bear on the question. Start from the catalog, not a blind
read of every file:

- Read `wiki/index.md` — it lists every page grouped by type with a one-line
  summary. Use it to pick candidate `summary`, `entity`, `concept`, and
  `analysis` pages.
- Read the bodies of the candidate pages you picked.
- **Fall back to Grep over `wiki/`** when the index's one-line summaries are too
  coarse to tell whether a page is relevant — search page bodies for the
  question's key terms and read what matches.

Do **no** `wiki/` writes in this phase.

### 2. Synthesize

Compose an answer grounded in what those pages actually say:

- Cite the pages you draw on with inline Obsidian `[[wikilinks]]` that resolve by
  filename. Every cited claim must trace to a real page.
- Keep the synthesis to what the corpus supports.

### 3. Be honest about coverage

The wiki's credibility depends on this — never pass outside knowledge off as
corpus-backed:

- **If the corpus does not cover the question**, say so plainly rather than
  fabricating a cited answer. Suggest filing a source with `/file` to close the
  gap.
- **If coverage is only partial**, answer what the corpus supports and name the
  gap. If you supplement with outside knowledge, mark that portion explicitly as
  *not corpus-backed* and give it no `[[wikilink]]` citation.

---

## Phase 2 — file the answer (optional: propose → coach → commit)

After answering, offer to file the answer as an `analysis` page. If the user
only wanted a lookup, stop here — nothing is written.

### 1. Propose

Survey the wiki so your proposal fits the corpus (you have already read the
relevant pages; now scan tags). Present:

- **Page type** — `analysis`.
- **Title** — the human-readable title (the wiki slug derives from it).
- **Tags** — drawn from existing tags where they apply. **Flag every genuinely
  new tag explicitly** ("new tag: …") so the user can approve or redirect it.
- **Sources** — the `[[wikilinks]]` the answer cites.
- **Draft `## Answer`** — your corpus-grounded synthesis from Phase 1.

### 2. Coach

Let the user revise anything: re-title, re-tag, add or drop a cited source,
reword the answer. Iterate until they are satisfied.

**Solicit the "Why this matters" commentary.** Ask the user, in their own words,
why this question or its answer is interesting. This becomes the `## Why this
matters` section and must be the user's voice, not yours. Do not commit without
it.

### 3. Commit

Only after the user says to file it, write all of the following. (Use
`templates/analysis.md` as the starting shape.)

1. **`wiki/analyses/<slug>.md`** — `<slug>` from the final title (no date
   prefix). Front-matter per `CLAUDE.md`: `type: analysis`, `title`, `created`
   (today), `question` (the original question, verbatim), `tags`, `sources`
   (the cited `[[wikilinks]]`). Body has exactly two sections: `## Answer` (your
   synthesis, with inline `[[wikilinks]]`) and `## Why this matters` (the user's
   commentary). If the slug collides with an existing page, append `-2`, `-3`, …

2. **Back-links from cited hubs** — for each `entity`/`concept` hub the analysis
   materially extends, add a `[[wikilink]]` back to this analysis under its
   Sources. Use judgment: a hub the answer merely name-drops need not be edited.
   Never duplicate an existing link, and never edit a `raw/` twin.

3. **`wiki/index.md`** — add the new page under the `## Analyses` grouping as a
   `[[wikilink]]` plus a one-line summary. Replace the `_None yet._` placeholder
   if it is still there.

4. **`wiki/log.md`** — append one entry (do not rewrite existing ones):
   `## [<date>] query: <subject>` followed by a line noting the question and the
   pages cited.

Validate before finishing: the page's `type` is `analysis`, both `## Answer` and
`## Why this matters` are present, and every `[[wikilink]]` points to a real or
just-touched page filename. Keep each `[[wikilink]]` on a single line — Obsidian
does not resolve a link split across a line break, so never let line wrapping
break one. If anything is off, fix it rather than committing a broken page.

---

## Guardrails

- Phase 1 answers in conversation and writes nothing; never touch `wiki/` until
  the user commits in Phase 2.
- Ground every cited claim in a real page. Never fabricate a `[[wikilink]]`
  citation, and mark any outside knowledge as not corpus-backed.
- When the corpus does not cover the question, say so — do not invent an answer.
- A `type` outside `summary|entity|concept|analysis` is invalid — halt and
  report instead of writing.
- Raw twins are immutable: never edit or rename a file under `raw/`.
- Filing an analysis must update both `index.md` and `log.md`.
