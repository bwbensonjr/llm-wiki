## Context

Today `file` is a two-phase command: Phase 1 mechanically converts a source to an
immutable `raw/` twin (Python, `wiki_ingest/`), Phase 2 is an LLM interview that
authors the `wiki/` layer only on the curator's commit. The split is clean —
**Python does the mechanical work, the skill does the judgment** — and it is worth
preserving.

The constraint that shapes this design: the wiki layer is authored by *judgment*,
not by a converter. There is no way to produce a summary, choose hubs, or draft
significance without an LLM in the loop. So "unattended ingest" cannot be a Python
batch job that the skill later blesses; it is the same skill logic with the
interview removed, driven headlessly. Everything below follows from that.

Current corpus state for migration purposes: 19 summaries, 21 concepts, 7
entities, 1 analysis, 16 raw twins. No page carries a `status:` field today.

```
  BEFORE                          AFTER
  ──────                          ─────
  link ──▶ capture ──▶ INTERVIEW  inbox.md ──▶ capture ──▶ author
              │           │          │                       │
              ▼           ▼          ▼                       ▼
           raw/twin    wiki/      raw/twin           wiki/ status:provisional
                                                             │
                       ▲                                     ▼
                       │                              commit + push ──▶ live
                  one sitting,                               │
                  one source                                 ▼
                                                   curate (batch, offline)
                                                             │
                                                             ▼
                                                     status: reviewed
```

## Goals / Non-Goals

**Goals:**

- Decouple capture cadence from review cadence; the curator's judgment is moved,
  not removed.
- Make the review queue *derived* state, so it cannot drift from the corpus.
- Keep every existing invariant: `raw/` immutability, converter routing, the
  four-type taxonomy, the mechanical image filter, `lint`'s contract.
- Make unattended runs safely repeatable — interrupted, re-run, and idempotent.
- Keep the Python/skill split intact; add as little Python as possible.

**Non-Goals:**

- **Scheduling.** How the unattended run is triggered (`cron`, the `schedule`
  skill, manual invocation) is out of scope. The design only requires that the
  command be *safely runnable headlessly*; picking a scheduler is a later,
  separate decision.
- **Source discovery.** No RSS, newsletter, or feed crawling. The curator still
  chooses every link — `inbox.md` is a queue of human-chosen sources. This keeps
  the CLAUDE.md premise ("the human curates sources") intact; automating
  discovery too would make this a firehose rather than a faster cadence, and is a
  different change.
- **Changes to `lint`.** See the proposal — provisional is not a defect.
- **Staged or filtered publishing.** Provisional pages go live.
- **Rewriting existing pages' content.** Migration only adds a front-matter field.

## Decisions

### 1. Review state is front-matter; the queue is derived

`status: provisional | reviewed` on every knowledge page. The review queue is the
result of scanning front-matter, never a maintained list.

*Why:* `index.md` is already maintained state, and `lint` exists in part because
maintained state drifts. Adding a `review-queue.md` would create a second file
that can disagree with the corpus, and a second thing for `lint` to reconcile. A
derived queue is idempotent, survives interruption mid-batch, needs no cleanup
step, and cannot lie.

*Alternative considered:* a staging folder (`wiki/inbox/`) that pages move out of
on review. Wikilinks resolve by filename, so moving pages between folders is
actually link-safe — but it breaks the "folders mirror `type`" rule that gives
the system its unambiguous write-here rule, and `lint` would report every staged
page as a folder/type mismatch. Rejected.

*Alternative considered:* using git history (`git log` since last review) to
define "recent additions." Rejected: it makes the queue a function of review
*time* rather than review *state*, so an interrupted review loses its place, and
a page skipped once is never seen again.

### 2. `status` marks the page; the body prose stays clean

The drafted `## Why this matters` is written as ordinary prose, with no inline
"LLM-drafted" disclaimer in the body. The front-matter `status` is the sole
marker.

*Why:* endorsement should be a one-field edit, not "delete the disclaimer line and
hope you got it." A disclaimer in the body means every endorsement is a body edit
and any missed one is a permanent lie in the page. Keeping the signal in exactly
one place makes the two states mechanically distinguishable and cheap to flip.

*Trade-off:* a reader who ignores front-matter cannot tell drafted significance
from endorsed significance. Surfacing `status` on the published site is the
mitigation (see Open Questions).

### 3. The inbox note seeds the drafted commentary

`inbox.md` lines take the form:

```markdown
- [ ] https://example.com/paper.pdf — worth it for the CPS angle
- [ ] https://example.com/post
- [x] https://example.com/already-ingested
- [!] https://example.com/broken — 2026-08-05: docling failed, unparseable PDF
```

Everything after the URL and an em-dash/hyphen separator is an optional curator
note. When present it seeds the drafted `## Why this matters`.

*Why:* that note is the only genuine curator voice available at unattended ingest
time, and it costs nothing to capture — the curator is already typing it or
already isn't. It is the difference between provisional significance that is
purely machine-inferred and provisional significance anchored to why the link was
actually saved.

*Why a checklist rather than draining lines:* `- [x]` keeps the file
human-legible and diffable, makes re-runs naturally idempotent, and preserves the
record of what was queued. `- [!]` plus a dated reason parks a permanently
failing link so it stops being retried on every run without silently vanishing.

*Location:* repo root, committed. Deliberately **not** under `wiki/` — it is not a
knowledge page, Quartz would publish it, and `lint` would report it as missing a
`type`. It is committed rather than ignored so the curator can append from
another machine.

### 4. The batch loop lives in the skill; Python stays mechanical

`wiki-capture` keeps its single-source signature. The unattended skill parses
`inbox.md`, checks for duplicates, calls `wiki-capture` per link, authors the
pages, and rewrites the inbox checkboxes.

*Why:* the authoring step is irreducibly LLM judgment, so the loop body has to be
in the skill regardless. Putting the loop in Python would mean Python invoking an
LLM per item — inverting the existing architecture for no gain. Inbox parsing is
a handful of Markdown lines and duplicate detection is a `source:` grep; neither
justifies new Python surface.

*Consequence:* the unattended run is a headless Claude Code invocation. The
command must therefore be written to never ask a question — any ambiguity
resolves to a documented default or to skipping that link with an inbox
annotation, never to a prompt that would hang a scheduled run.

### 5. Duplicate detection matches on `source:`

Before capturing, skip any inbox link whose URL already appears as the `source:`
of an existing summary; check it off with a note saying so.

*Why:* a checked-off queue plus re-runs plus a curator who pastes the same link
twice makes double-ingest likely. Matching `source:` catches it at the only place
identity is recorded. Cheap, and it protects `raw/` from accumulating redundant
twins.

*Limitation accepted:* URL-string identity misses the same document at two URLs
(arXiv abs vs pdf, a syndicated repost). `curate` catches those as near-duplicate
summaries during review; no attempt is made to canonicalize URLs mechanically.

### 6. Hub status: created-provisional, but never thrashed back

A hub created by an unattended ingest is `status: provisional`. A hub that is
already `reviewed` and merely gains a Sources backlink from a later unattended
ingest **stays `reviewed`**.

*Why:* unattended ingest must be allowed to create hubs — the hub graph *is* the
wiki's compounding value, and a link-only policy would land a batch of related
sources as disconnected leaves. But new hubs are also the real
corpus-pollution vector (`chris-lattner` vs `christopher-lattner`), so they must
be reviewable. Reverting a settled hub to provisional on every backlink would
mean popular hubs are permanently unreviewed and the queue never drains — the
status would stop meaning anything.

### 7. `curate` is its own command, not a `lint` mode

*Why:* `lint`'s spec guarantees that a clean corpus reports no defects. A
provisional page is not a defect, so folding the queue into `lint` would make an
auto-ingesting wiki permanently "dirty" and kill the signal that makes `lint`
worth running. The verbs differ too: `lint` *repairs*; `curate` *endorses,
reclassifies, and rejects* — and rejection (deleting a page) is not a repair.
`curate` reuses `lint`'s established shape (read-only survey, propose → coach →
commit, one appended `## [<date>] curate:` log entry) without inheriting its
contract.

*Naming:* `review` collides with a built-in Claude Code PR-review skill; `audit`
implies read-only. `curate` names what the human uniquely does here.

### 8. Rejection deletes and logs; `raw/` survives

Rejecting a page deletes the summary file, removes its `index.md` entry, removes
its backlink from every hub that cites it, and appends a `curate` log entry naming
the source and the reason. Any hub created solely by that ingest and left with no
remaining sources is deleted too. The `raw/` twin and `raw/assets/` bytes remain —
immutable, as always. No tombstone page.

*Why no tombstone:* this is an information source, not a system of record. The log
entry plus git history is sufficient evidence, and a corpus of tombstones for
rejected auto-ingests would be noise. The surviving `raw/` twin also means a
rejection is recoverable without refetching.

### 9. Per-source commits, one push per batch

Each ingested source gets its own commit in the existing `Ingest: <title>` style;
the batch pushes once at the end.

*Why:* per-source commits keep git a per-source audit trail — reviewing "what did
the machine do" is reading a diff — and let a mid-batch failure leave completed
work committed. A single push at the end minimizes the number of Pages deploys a
batch triggers.

## Risks / Trade-offs

- **Queue debt: ingest outpaces curation.** A cadence faster than the curator's
  review rhythm means a growing pile of provisional pages, and the wiki's average
  quality drifts toward machine-judged. → Mitigation: `curate` reports queue size
  and age, so the debt is visible rather than silent; the curator throttles by
  how much they put in `inbox.md`. This is the central risk of the whole change
  and no mechanism fully removes it — the honest control is the inbox.

- **Hub near-duplicates accumulate between reviews.** Unattended ingest cannot
  see hubs a *concurrent* item in the same batch is about to create, and will
  mint slug variants over successive runs. → Mitigation: within a batch, ingest
  processes links sequentially so each sees hubs created by the previous;
  `curate` clusters near-duplicate hub slugs across the queue and offers merges,
  reusing the clustering approach `lint` already specifies for tags.

- **A garbage or paywalled fetch becomes a plausible published page.** Jina
  returning a cookie wall or a paywall stub yields a confidently-written summary
  of nothing, live on the site. → Mitigation: the unattended path should refuse
  to author on an implausibly thin or boilerplate-looking twin, annotating the
  inbox line instead; `provisional` status and the `reject` verb catch what slips
  through. Worth an explicit spec requirement.

- **Push races with local work.** A scheduled run pushing to `main` while the
  curator has unpushed local commits. → Mitigation: rebase on the remote before
  pushing and abort the push loudly on conflict, leaving commits local. Never
  force-push; never resolve a content conflict unattended.

- **Endorsement becomes rubber-stamping.** If review is a wall of pre-written
  prose to click through, the curator's voice quietly becomes the LLM's. →
  Mitigation: `curate` presents *corpus-relational* observations (what this
  connects to, what it duplicates, what it contradicts) rather than just
  restating the draft, so review is a judgment prompt rather than an approval
  queue. Accepted residual risk: this is the curator's discipline to keep, and it
  is the trade the change deliberately makes.

- **A headless run that asks a question hangs forever.** → Mitigation: the
  unattended path is specified to have no interactive branches at all; every
  ambiguity has a documented default or skips the link.

## Migration Plan

1. Add `status:` to `templates/summary.md`, `entity.md`, `concept.md`,
   `analysis.md`.
2. Backfill every existing `wiki/` knowledge page with `status: reviewed` — all
   47 were authored through the interview, so they are endorsed by construction.
   Front-matter-only edit; no body changes.
3. Create `inbox.md` at the repo root with the format documented in a header
   comment, plus an empty checklist.
4. Land `curate` **before** the unattended ingest path. It is the drain; shipping
   the faucet first with no drain is how queue debt becomes unrecoverable.
5. Land unattended ingest and exercise it manually on a small inbox (2–3 links)
   before any scheduling is considered.

*Rollback:* the change is additive. Stop putting links in `inbox.md` and the
system reverts to interactive `file`. `status: reviewed` is inert on the old path.
Individual bad ingests roll back via `curate --reject` or `git revert` of that
source's commit.

## Open Questions

- **Surfacing `status` to site readers.** The proposal argues provisional pages
  going live makes `status` a reader-facing honesty signal, but Quartz v4 does not
  render arbitrary front-matter and `quartz.config.ts` is meant to stay minimal.
  Options: a small Quartz component, a `provisional` tag riding along in `tags:`
  (visible and filterable, but duplicates state), or accepting for now that
  `status` is only visible in the repo. Deferred — it does not block the queue
  mechanics.
- **Batch size cap per run.** Unbounded, or a limit so one run cannot add 50
  provisional pages? Leaning unbounded, since the inbox is already the curator's
  throttle.
- **Whether `curate` should also handle interactive-path pages.** Nothing
  produces a provisional page except unattended ingest today, so the question is
  moot until something else does.
