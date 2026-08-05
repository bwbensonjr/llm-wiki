---
name: ingest-inbox
description: Drain the llm-wiki inbox queue unattended. Reads inbox.md, skips already-ingested sources, captures each remaining link into an immutable raw twin, then authors provisional wiki pages with no interview — classifying, tagging, linking hubs, judging figures, and drafting significance on its own — committing per source and pushing once at the end. Use when the user wants to run the batch ingest, drain the inbox, or ingest queued links unattended.
metadata:
  author: llm-wiki
  version: "1.0"
---

# The `ingest-inbox` command

Drain `inbox.md` without a curator present. This is the same authoring work the
`file` command does, with the interview removed and the judgment taken on by you.
Read the repo `CLAUDE.md` first — page taxonomy, the `status` field, front-matter
schemas, slug rules, tag conventions, and image handling are binding here.

**This command runs headlessly. It has no interactive branches at all.** Every
ambiguity resolves to a documented default or parks that entry with a reason.
Never ask a question: a scheduled run that asks one hangs forever. If you find
yourself about to prompt, park the entry instead and move on.

Everything this command writes to `wiki/` is `status: provisional`. That is the
whole safety model: the pages publish immediately, and the curator endorses,
corrects, or rejects them later via `curate`.

---

## Step 1 — parse the inbox

Read `inbox.md` at the repo root. Consider **only** lines matching `- [ ]`.
Entries marked `- [x]` (ingested) or `- [!]` (parked) are done — skip them
silently; they are never retried.

Split each unprocessed line into:

- **source** — the leading URL or local path, and
- **note** — everything after a ` — ` or ` - ` separator, if any. Free text; the
  curator's reason for saving the link.

Ignore everything outside the checklist: the file's header prose, the format
table, and the fenced example block are documentation, not queue entries. A line
whose source does not parse as a URL or an existing local path is parked
(`- [!]`) with that reason rather than guessed at.

Process entries **sequentially**, not in parallel — each entry must see the hubs
created by the one before it, or a batch of related sources mints slug variants
of the same hub.

There is no batch cap. The inbox is the curator's throttle.

---

## Step 2 — per entry

Everything below is scoped to one entry. **Each entry is independent:** any
failure parks that entry and continues the run. Never abort the batch, and never
discard or roll back work already committed for earlier entries.

### 2a. Skip duplicates

Before capturing, grep existing summary front-matter for the entry's source:

```bash
grep -rl "^source: <the-url-or-path>" wiki/summaries/
```

If it matches an existing summary's `source:`, this link is already in the wiki.
Write **no** `raw/` twin and **no** `wiki/` page. Mark the entry `- [x]` with an
annotation naming the existing page (`already ingested as [[<slug>]]`) and move
to the next entry.

Match on the URL/path string. Identity is only recorded there, so the same
document under two URLs (arXiv `abs` vs `pdf`, a syndicated repost) will not be
caught here — that is accepted, and `curate` catches it as a near-duplicate
summary at review. Do **not** try to canonicalize URLs.

### 2b. Capture (mechanical, unchanged)

Run the converter exactly as `file` does — same single-source signature, same
routing, same automatic image localization:

```bash
uv run wiki-capture "<source>"
```

- **On success** it prints JSON: `{"raw_path", "converter", "detected_type",
  "title", "images"}`. Parse it; keep `raw_path` and the `images.kept` list.
- **On failure** it prints `{"error": ...}` to stderr, exits non-zero, and has
  written nothing. Park the entry with the error and go to the next one.

### 2c. Refuse an implausible capture

Read the twin at `raw_path` and judge whether it is actually the source. Refuse
to author when the twin is:

- **implausibly thin** for what the source claims to be — a few lines where an
  article or paper was expected;
- a **cookie-consent or paywall stub**, a **login wall**, a captcha or bot check;
- an **error page** (404/403/500 rendered as content);
- otherwise boilerplate navigation with no substance.

On refusal: write **no** `wiki/` pages, park the entry `- [!]` with the reason
(`2026-08-05: paywall stub, no article content`), and continue. **Leave the twin
in place** under `raw/` — it was already written and is immutable; it is also the
evidence for why the entry was parked.

This check is the difference between a bad fetch and a confidently-written
published summary of nothing. When genuinely uncertain, park it: a parked entry
is visible and retryable by hand, a bogus summary is corpus damage.

### 2d. Author the wiki layer — no interview

Survey the corpus first so the page fits it: `wiki/index.md`, existing hubs under
`wiki/entities/` and `wiki/concepts/`, and the tag vocabulary already in use.
Then decide, on your own judgment:

- **Type** — `summary` for an ingested source. A `type` outside
  `summary | entity | concept | analysis` is invalid: park the entry rather than
  write it.
- **Title** — the human-readable title; the wiki slug derives from it. On slug
  collision append `-2`, `-3`, …
- **Tags** — **prefer existing tags**; mint a new one only when nothing in the
  vocabulary fits. Approval is deferred, not skipped (see 2f).
- **Wikilinks** — link existing hubs wherever the source touches them. Create a
  new hub when the source genuinely warrants one: the hub graph is the wiki's
  compounding value, and link-only ingest lands a batch of related sources as
  disconnected leaves. Match an existing hub before minting a variant of it
  (`chris-lattner`, not a second `christopher-lattner`).
- **`## Summary`** — your neutral distillation, with inline `[[wikilinks]]`.

### 2e. Figures (Jina route only)

If capture localized images (`images.kept` non-empty), that judgment is yours —
there is no interview to review them:

- `Read` the localized figures under `raw/assets/<twin-stem>/`.
- **Distill** the meaningful ones into `## Summary` as prose — describe or
  transcribe what the figure shows. The wiki layer is a distillation, not a copy.
- **Drop** the rest. A dropped figure is neither distilled nor promoted; its
  `raw/assets/` bytes stay put, immutable.
- **Promote** only a figure whose meaning prose cannot carry — a diagram,
  schematic, or plot that must be *seen*. Copy that one file into `wiki/assets/`
  (create the directory on first use) and embed it with an Obsidian image link.
  Never bulk-copy a source's images. The `raw/assets/` original stays the source
  of truth.

Record both decisions — what you distilled, what you promoted — in the log entry
(2g), so they are visible at review and reversible via `curate`.

### 2f. Draft `## Why this matters`

- **With a curator note:** the note is the basis of the section. It is the only
  genuine curator voice available at unattended ingest time — preserve its stated
  reason rather than replacing it with your own reading, and expand it into prose
  rather than quoting it verbatim.
- **Without one:** infer significance from the source and its relationship to the
  existing corpus — what it extends, corroborates, or contradicts among pages
  already here. The page is still written and still `provisional`.

Write it as ordinary prose. **No inline authorship disclaimer** — `status:` is the
sole marker, so endorsement stays a one-field edit and no stale disclaimer can
survive review.

### 2g. Write the pages

1. **`wiki/summaries/<slug>.md`** — front-matter per `CLAUDE.md`:
   `type: summary`, **`status: provisional`**, `title`, `created` (today),
   `source`, `raw: <raw_path>`, `tags`. Body has exactly `## Summary` and
   `## Why this matters`.

2. **Hub pages** the summary touches:
   - **Created** by this ingest → write it from the template with
     **`status: provisional`**.
   - **Existing** hub → append the `[[wikilink]]` backlink under its `## Sources`
     and any warranted note. If that hub is `status: reviewed`, **leave it
     `reviewed`.** Never revert a settled hub to provisional for a routine
     backlink — popular hubs would be permanently unreviewed and the queue would
     never drain.

3. **`wiki/index.md`** — add each new page under its type grouping, as a
   `[[wikilink]]` plus a one-line summary.

4. **`wiki/log.md`** — append one entry (never rewrite existing ones):

   ```markdown
   ## [<date>] ingest: <title>
   ```

   Its body must record: the source URL, the converter used, **that the run was
   unattended**, **every tag this ingest newly minted** (this is the deferred tag
   approval `curate` acts on — if it is not logged, the new vocabulary is
   invisible), any hubs created, and any figure promoted to `wiki/assets/`.

Validate before committing: `type` and `status` are valid values, both body
sections are non-empty, and every `[[wikilink]]` resolves to a real or
just-created page filename. Keep each `[[wikilink]]` on one line — Obsidian does
not resolve a link split across a line break. If validation fails, fix it; if it
cannot be fixed, park the entry and leave no half-written page behind.

### 2h. Commit this source

One commit per source, in the existing style:

```bash
git add <the specific paths written> && git commit -m "Ingest: <title>"
```

Stage explicit paths — never `git add -A`. Per-source commits keep git a
per-source audit trail, and mean a later failure leaves this work safely
committed.

### 2i. Write back to the inbox

Update this entry's checkbox **in place**, never deleting the entry:

- success → `- [x] <source> — <note>`
- already ingested → `- [x] <source> — already ingested as [[<slug>]]`
- failure or refusal → `- [!] <source> — <YYYY-MM-DD>: <reason>`

A parked entry stops being retried on every run while staying visible to the
curator. Include the inbox change in that source's commit.

---

## Step 3 — end of run

### Push once

If at least one source was committed:

```bash
git pull --rebase && git push
```

One push per batch, so a batch triggers one Pages deploy rather than one per
source.

**On conflict:** abort. Leave the commits local, report the conflict, and stop.
**Never force-push. Never resolve a content conflict unattended.** Local commits
are recoverable; a force-push over the curator's work is not.

If no source was committed, push nothing.

### Report

Emit a per-entry outcome summary — one line per entry: ingested (with the page
slug), skipped as duplicate, or parked (with the reason) — plus whether the push
succeeded, was skipped, or aborted on conflict.

---

## Guardrails

- **No interactive branches.** Never ask a question; park the entry instead.
- **`status: provisional`** on every page this path creates. An existing
  `reviewed` hub gaining only a backlink stays `reviewed`.
- **Raw twins are immutable** — never edit or rename anything under `raw/`,
  including the twin of an entry you refused to author from.
- **Failure isolation** — one entry's failure never aborts the run or discards
  another entry's committed work.
- **Never delete an inbox entry**; the checkbox carries the state.
- **A drained inbox is a no-op** — no file under `raw/` or `wiki/` is created or
  modified, and nothing is committed or pushed.
- Refuse to author from an implausible twin rather than publishing a confident
  summary of a paywall.
- A `type` or `status` outside the allowed set is invalid: park, do not write.
- Never `git add -A`; never force-push; never resolve a conflict unattended.
