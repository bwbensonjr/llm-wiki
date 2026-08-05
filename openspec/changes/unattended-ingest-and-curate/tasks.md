## 1. Establish the review-state primitive

- [x] 1.1 Add `status: <provisional | reviewed>` to `templates/summary.md`,
      `templates/entity.md`, `templates/concept.md`, and `templates/analysis.md`
- [x] 1.2 Document the `status` field in `CLAUDE.md`: allowed values, that
      `provisional` means machine-authored and `reviewed` means curator-endorsed,
      and that an out-of-set value is invalid (halt and report)
- [x] 1.3 Add `status:` to all four literal front-matter YAML blocks in
      `CLAUDE.md` (summary, entity, concept, analysis) so the documented schema
      matches the templates
- [x] 1.4 Rewrite the `CLAUDE.md` description of `## Why this matters` to be
      endorsement-gated rather than authorship-gated, and state that the body
      carries no inline authorship disclaimer
- [x] 1.5 Rewrite the `CLAUDE.md` opening framing of the human/LLM division of
      labor — the LLM now also judges and files unattended, and the human reviews
      afterward rather than at capture time
- [x] 1.6 Rewrite the `CLAUDE.md` tag rule: new tags are approved before commit on
      the interactive path, but *deferred* to `curate` on the unattended path via
      `provisional` status and a log record — never silently minted
- [x] 1.7 Rewrite the `CLAUDE.md` Image-handling claim that "the Phase 2 interview
      is the review/consent point" for figures — true on the interactive path only;
      state that unattended figure judgment is the LLM's, logged and reversible
- [x] 1.8 Backfill `status: reviewed` into the front-matter of every existing
      `wiki/` knowledge page (summaries, entities, concepts, analyses) —
      front-matter only, no body edits
- [x] 1.9 Verify the backfill: every knowledge page has exactly one `status:`
      line with a valid value, and `git diff` shows no body changes

## 2. Curate command (the drain — lands before the faucet)

- [x] 2.1 Add a `## [<date>] curate: <subject>` entry convention to the `log.md`
      section of `CLAUDE.md`, alongside the existing `ingest` and `lint` ops
- [x] 2.2 Create `.claude/skills/curate/SKILL.md` with the queue-derivation step:
      scan `wiki/` front-matter for `status: provisional`, report queue size and
      oldest-entry age, write nothing by default
- [x] 2.3 Implement the corpus-relational presentation: for each queued page,
      surface its hub links, overlapping/duplicate existing pages, and pages it
      extends or contradicts — not merely a restatement of the drafted text
- [x] 2.4 Implement duplicate-hub clustering across the queue and against
      existing hubs (casing, punctuation, name-form, abbreviation, plural
      variants), proposing a canonical page per cluster without merging
- [x] 2.5 Implement the review verbs: endorse, edit-then-endorse, retag,
      reclassify (with folder re-filing and `index.md` regrouping), merge-hub,
      reject
- [x] 2.6 Implement merge-hub application: rewrite every inbound `[[wikilink]]`
      to the canonical page, carry over Sources backlinks, delete the variant,
      update `index.md`
- [x] 2.7 Implement reject application: delete the page, remove its `index.md`
      entry, strip its backlink from every citing hub, delete hubs orphaned by
      the rejection, remove any `wiki/assets/` copy the page had promoted, leave
      `raw/` and `raw/assets/` untouched, no tombstone
- [x] 2.8 Implement the propose → coach → commit gate: preview all intended
      changes, write nothing without an explicit commit, append exactly one
      `curate` log entry recording endorsements, merges, and rejections with
      reasons
- [x] 2.9 Add guardrails to the skill: never edit or rename anything under
      `raw/`, never repair structural defects (that is `lint`'s job), leave
      undecided pages `provisional`

## 3. Inbox queue

- [x] 3.1 Create `inbox.md` at the repo root: a header comment documenting the
      line format (`- [ ]` unprocessed, `- [x]` ingested, `- [!]` parked, URL
      followed by an optional separator and curator note) plus an empty checklist
- [x] 3.2 Document `inbox.md` in `CLAUDE.md`: its purpose, why it lives at the
      root rather than under `wiki/` (not a knowledge page, not published, not
      linted), and that it is committed mutable working state
- [x] 3.3 Confirm `inbox.md` is committed and not swept into `.gitignore`, and
      that a site build does not publish it

## 4. Unattended ingest path

- [x] 4.1 Create `.claude/skills/ingest-inbox/SKILL.md` covering inbox parsing:
      read `- [ ]` entries only, split each into source and optional curator note
- [x] 4.2 Implement duplicate detection: skip an entry whose URL/path already
      appears as an existing summary's `source:`, writing no `raw/` twin and
      checking the entry off as already ingested
- [x] 4.3 Implement the per-entry capture step by calling the existing
      `uv run wiki-capture "<source>"` unchanged, parsing its JSON result
- [x] 4.4 Implement the implausible-capture refusal: detect a thin, cookie-wall,
      paywall, login, or error-page twin, write no `wiki/` pages, park the entry
      with the reason, leave the twin in place
- [x] 4.5 Implement non-interactive authoring: type, title, tags preferring the
      existing vocabulary, `[[wikilinks]]` to existing hubs, creation of new hubs
      as warranted, and a drafted `## Summary`
- [x] 4.5a Record every newly-minted tag in that ingest's `wiki/log.md` entry, so
      the tag approval deferred from ingest is visible to `curate`
- [x] 4.6 Implement drafted `## Why this matters`, seeded by the entry's curator
      note when present and inferred from source-plus-corpus when absent
- [x] 4.7 Implement autonomous figure handling on the Jina route: judge which
      localized figures carry meaning, distill those into `## Summary`, promote
      only figures prose cannot replace into `wiki/assets/`, record promotions in
      the log entry
- [x] 4.8 Write `status: provisional` on every page the path creates; write
      `status: provisional` on newly created hubs; leave an existing
      `status: reviewed` hub at `reviewed` when only appending a Sources backlink
- [x] 4.9 Implement bookkeeping per entry: `index.md` entry, `wiki/log.md` entry
      marked as unattended, and one git commit in the existing `Ingest: <title>`
      style
- [x] 4.10 Implement inbox writeback: mark each entry `- [x]` on success or
      `- [!]` with date and reason on failure; never delete an entry
- [x] 4.11 Implement per-entry failure isolation so one failure never aborts the
      run or discards completed work, and emit a per-entry outcome summary
- [x] 4.12 Implement the end-of-run push: rebase on the remote, push once,
      abort loudly on conflict leaving commits local, never force-push, never
      resolve a content conflict
- [x] 4.13 Audit the whole skill for interactive branches and remove them — every
      ambiguity must resolve to a documented default or a parked entry, so a
      headless run can never hang on a prompt

## 5. Verification

- [x] 5.1 Verify idempotence: run against a fully drained inbox and confirm no
      files under `raw/` or `wiki/` are created or modified
- [ ] 5.2 Verify failure isolation with a deliberately broken link alongside two
      good ones: both good entries land, the broken one is parked with a reason
- [x] 5.3 Verify duplicate skip using a URL already present as an existing
      summary's `source:`
- [ ] 5.4 Exercise the full path manually on a small inbox of 2–3 real links,
      inspecting the resulting diff before allowing the push
- [ ] 5.5 Run `curate` against the resulting provisional queue and exercise each
      verb at least once, including a reject, confirming the `raw/` twin survives
- [ ] 5.6 Run `lint` over the corpus with provisional pages present and confirm it
      reports clean — provisional is not a defect
- [x] 5.6a Confirm `CLAUDE.md` contains no surviving statement that contradicts the
      unattended path: reread it end to end against the change, since it is binding
      on every operation that reads or writes wiki content
- [x] 5.7 Build the site and confirm provisional pages publish and `inbox.md` does
      not

## 6. Documentation

- [x] 6.1 Update the `README.md` Principles list, which still describes ingest as
      inherently interactive, and add the two new commands to the Commands list
      with the capture-cadence / review-cadence split
- [x] 6.2 Document in `CLAUDE.md` that `lint` audits structure while `curate`
      exercises judgment, and that the two are deliberately orthogonal
- [x] 6.3 Record the deferred decisions from `design.md` open questions —
      surfacing `status` to site readers, and any per-run batch cap — as
      follow-up notes rather than silently dropping them
