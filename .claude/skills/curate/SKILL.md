---
name: curate
description: Review the llm-wiki's provisional queue. Derives the set of pages carrying status provisional, presents each with its corpus-relational context and any newly-minted tags, clusters near-duplicate hubs, and applies endorse / edit / retag / reclassify / merge-hub / reject decisions through a propose→coach→commit interview. Use when the user wants to curate, review, endorse, or reject machine-authored wiki pages.
metadata:
  author: llm-wiki
  version: "1.0"
---

# The `curate` command

Drain the **provisional queue**: the pages the unattended ingest path authored
without a curator present. Read the repo `CLAUDE.md` first — the page taxonomy,
per-type front-matter, the `status` field, slug rules, folder→type mapping, and
tag conventions are binding here.

`curate` exercises **judgment**; `lint` audits **structure**. They are
deliberately orthogonal. A `status: provisional` page is not a defect, and a
broken wikilink is not a review decision. Do not do `lint`'s job here.

**Input:** an optional scope argument (a page, a folder, or a count). With none,
survey the whole queue.

**The command always surveys and reports first. Nothing is written until the
curator commits.**

---

## Phase 1 — derive the queue (read-only)

Do **no** writes in this phase.

Glob `wiki/**/*.md` **from disk** — never from `index.md`, which is maintained
state and may itself be stale. Parse each page's YAML front-matter. The queue is
exactly the set of knowledge pages carrying `status: provisional`. There is no
queue file and you must never create one: the queue is derived state, so it
cannot drift from the corpus, and an interrupted review needs no cleanup — the
pages left undecided are still provisional and simply reappear next run.

Report up front, before any per-page detail:

- **Queue size** — how many pages await review, broken down by `type`.
- **Oldest entry** — the earliest `created:` date in the queue and its age in
  days.

That pair is the review-debt signal. If ingest is outpacing curation, this is
where it becomes visible rather than silent — say so plainly when the queue is
growing or the oldest entry is stale.

If no page carries `status: provisional`, report an empty queue, propose
nothing, and stop.

---

## Phase 2 — present with corpus-relational context

For each queued page, presentation must be a **judgment prompt, not an approval
queue**. Restating the drafted page is not review — the curator can read it. What
they cannot cheaply see is how it sits in the corpus. For each page present:

- **What it is** — title, type, tags, source, and a brief characterization of
  the drafted `## Summary` and `## Why this matters` (say when the latter was
  seeded by an `inbox.md` curator note, and quote that note).
- **What it links to** — the entity/concept hubs it `[[wikilinks]]`, marking
  which of those hubs this ingest **created** (they are provisional too, and are
  the real corpus-pollution vector).
- **What it overlaps** — existing summaries covering substantially the same
  material, near-duplicate hub slugs, and pages that this one **extends or
  contradicts**. Read the candidates before asserting a relationship; do not
  infer overlap from titles alone.
- **New tags** — every tag the page carries that appears nowhere else in the
  corpus, flagged explicitly as new. This is where the tag approval **deferred**
  at unattended ingest actually happens; the ingest's `wiki/log.md` entry names
  the tags that run minted, so cross-check against it.
- **Figure decisions** — any figure the unattended path promoted into
  `wiki/assets/` and embedded, so the curator can keep or drop it.

### Duplicate-hub clustering

Across the queue *and* against existing hubs, cluster hub pages that appear to
name the same entity or concept. Catch variants differing by:

- **casing** — `LLVM` / `llvm`
- **punctuation or separators** — `type-systems` / `type systems`
- **name form** — `chris-lattner` / `christopher-lattner`
- **abbreviation or expansion** — `mcp` / `model-context-protocol`
- **pluralization** — `neural-network` / `neural-networks`

For each cluster **propose** a canonical page and say why (usually the older,
more-linked, or already-`reviewed` page). **Never merge on your own** — the
canonical choice and the exact set of variants that fold into it is a curator
decision, made in Phase 3.

---

## Phase 3 — decide and apply (propose → coach → commit)

### 1. Propose

For each queued page, offer these verbs:

| Verb | Effect |
|------|--------|
| **endorse** | Accept as written. `status` → `reviewed`, nothing else changes. |
| **edit-then-endorse** | Revise the body first — most often replacing the drafted `## Why this matters` with the curator's own prose — then `status` → `reviewed`. |
| **retag** | Adjust `tags:`, typically redirecting a newly-minted tag to existing vocabulary. |
| **reclassify** | Change `type`, re-file the page into the folder mirroring the new type, and correct its `index.md` grouping. |
| **merge hub** | Fold a provisional hub into an approved canonical page. |
| **reject** | Remove the page entirely. |

A page the curator does not decide on **stays `provisional`** and reappears in
the next run's queue. Never endorse by default, never batch-endorse the queue
because it is long, and never treat silence as approval.

### Correcting a stale corpus claim

A **corpus-membership claim** — prose asserting what the wiki does or does not
contain, or a corpus-scoped superlative or count (see *Corpus independence* in
`CLAUDE.md`) — is correctable here, under **edit-then-endorse**. Propose the
correction whenever you find one on a page you are reviewing: name the offending
clause, and propose the repair shape, which is to state what is true of the subject
and drop the claim about the corpus. Leave sibling orientation alone — situating a
subject among related pages is conformant and is not a violation to fix.

**This applies to a page already carrying `status: reviewed`, and the page stays
`reviewed`.** That is a deliberate exception to `curate` acting on the provisional
queue, and the reason is the shape of the bug: this kind of claim is *true when
written and goes false later*, when some later ingest overturns it. So the page most
in need of correcting is frequently one the curator already endorsed in good faith —
the endorsement was sound, the corpus moved. Correcting it therefore does **not**
return the page to the queue: flipping it back to `provisional` would claim the
curator's judgment was wrong, and would swell a queue this command exists to drain.
Fix the clause, leave `status: reviewed`, and record it in the log entry.

Such a page is **not** a queue member — the queue stays exactly the set of
`status: provisional` pages derived in Phase 1. A reviewed page enters this run only
because reviewing a queued page surfaced the claim on a neighbor you read for context.
Do not go hunting the corpus for violations; that is a sweep, not a review.

**The narrow summary exception.** `CLAUDE.md` says a `summary` is written once at
ingest. Correcting one of these claims in a summary is permitted despite that, because
otherwise the write-once rule would preserve a known-false sentence indefinitely. The
permission is narrow: it extends to **removing or rephrasing the offending clause and
nothing else**. Do not revise the distillation, re-word the surrounding prose, or
refresh the summary against the source while you are in there. If the correction cannot
be made without rewriting the distillation, say so and leave the page alone rather than
stretching the exception.

### 2. Coach

Let the curator accept, adjust, or reverse any proposal, and revise prose
directly. For merges, confirm the canonical page and the exact variant set before
touching anything. For rejections, get the reason — it goes in the log. Iterate
until they are satisfied.

### 3. Preview, then commit

Before writing anything, **preview** the full intended change set — a per-file
change list or diff, including every link rewrite a merge implies and every file
a rejection deletes. Write only after an explicit commit. If the curator does not
commit, the wiki is left exactly as it was.

On commit, apply each decision:

**Endorse / edit-then-endorse / retag** — edit the page in place. Endorsement of
an unmodified page is a **single front-matter change**: `status: provisional` →
`status: reviewed`. There is no body disclaimer to strip; if you find one, that
is a bug in the ingest path, not a thing to work around silently. A stale
corpus-claim correction on an already-`reviewed` page is the mirror image: a body edit
with **no** front-matter change — `status` stays `reviewed`.

**Reclassify** — rewrite `type:`, move the file into the matching folder
(`wiki/summaries/`, `wiki/entities/`, `wiki/concepts/`, `wiki/analyses/`), and
move its `index.md` entry to the matching type grouping. Wikilinks resolve by
filename, so a move does not break links — but a rename does; if the slug must
change, rewrite every inbound `[[wikilink]]`.

**Merge hub** — for the folded variant:

1. Rewrite **every** inbound `[[wikilink]]` across the corpus to point at the
   canonical page. Grep the whole of `wiki/`; do not rely on the variant's own
   Sources list to find its inbound links.
2. Carry the variant's `## Sources` backlinks over to the canonical page,
   de-duplicating against what is already there.
3. Fold any unique prose from the variant's `## Notes` into the canonical page
   rather than discarding it.
4. Delete the variant file and remove its `index.md` entry.

**Reject** — the page is removed with no tombstone:

1. Delete the page file.
2. Remove its `index.md` entry.
3. Strip its backlink from **every** hub that cites it (grep the corpus for the
   slug; do not trust the page's own link list).
4. Delete any hub that this page's ingest created and that the rejection leaves
   with **no remaining sources** — an orphan hub minted for a page that no longer
   exists. A hub with other sources stays.
5. Delete any copy this page promoted into `wiki/assets/`, but **only** if no
   surviving page embeds it.
6. Leave `raw/` and `raw/assets/` **untouched** — the twin is immutable and its
   survival is what makes a rejection recoverable without refetching.
7. Write **no** tombstone or placeholder page. The log entry plus git history is
   the record.

**Log** — append exactly **one** entry to `wiki/log.md`, never rewriting existing
entries:

```markdown
## [<date>] curate: <subject>
```

followed by lines recording what was **endorsed**, what was **merged** (variant →
canonical), what was **rejected** and **why**, any tag redirects, and any **stale
corpus claim corrected** — naming the page, since a correction on an already-`reviewed`
page changes no front-matter and would otherwise leave no trace outside git history.
For a rejected page this log entry is the only surviving record in `wiki/`, so name the
source URL in it.

Name a **removed** page in plain text, not as a `[[wikilink]]` — the rejected page,
and the folded-away variant of a merge. Its slug in backticks. Per `CLAUDE.md`, the
log is append-only, so a link to a page you are deleting in the same entry is born
broken and can never be repaired. Pages that survive the run link normally.

After writing, re-check every page you touched: `status` is valid, `type` matches
its folder, required sections are present, and every `[[wikilink]]` you rewrote
resolves. Fix a regression rather than leaving a half-applied decision.

---

## Guardrails

- Phases 1–2 write nothing. Nothing is written in Phase 3 without an explicit
  commit.
- **Never edit or rename a file under `raw/`.** Twins are immutable — including
  the twin of a page you just rejected.
- **Do not repair structural defects.** A broken wikilink, a missing index entry,
  a `type`/folder mismatch on a page you are not reclassifying — all of that is
  `lint`'s job. Report it in passing if you like; do not fix it here. A
  corpus-membership claim is **not** in that category: reading prose for meaning is
  judgment, `lint` deliberately does not check it, and correcting it is this command's
  job.
- A corpus-claim correction on a `reviewed` page **leaves it `reviewed`**, and in a
  `summary` touches only the offending clause — never the distillation.
- Never merge hubs, redirect a tag, or reject a page without explicit approval.
- An undecided page stays `provisional`. Leaving the queue partly drained is a
  correct outcome.
- The queue is derived from `status:` on disk — never create a queue file, and
  never take the queue from `index.md`.
- A `status` outside `provisional | reviewed` or a `type` outside
  `summary | entity | concept | analysis` is invalid: halt and report.
- A committed run appends exactly one `## [<date>] curate: <subject>` entry to
  `wiki/log.md` and reflects every move, merge, and deletion in `index.md`.
