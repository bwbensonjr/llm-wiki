## 1. Establish the review-state primitive

- [ ] 1.1 Add `status: <provisional | reviewed>` to `templates/summary.md`,
      `templates/entity.md`, `templates/concept.md`, and `templates/analysis.md`
- [ ] 1.2 Document the `status` field in `CLAUDE.md`: allowed values, that
      `provisional` means machine-authored and `reviewed` means curator-endorsed,
      and that an out-of-set value is invalid (halt and report)
- [ ] 1.3 Add `status:` to all four literal front-matter YAML blocks in
      `CLAUDE.md` (summary, entity, concept, analysis) so the documented schema
      matches the templates
- [ ] 1.4 Rewrite the `CLAUDE.md` description of `## Why this matters` to be
      endorsement-gated rather than authorship-gated, and state that the body
      carries no inline authorship disclaimer
- [ ] 1.5 Rewrite the `CLAUDE.md` opening framing of the human/LLM division of
      labor — the LLM now also judges and files unattended, and the human reviews
      afterward rather than at capture time
- [ ] 1.6 Rewrite the `CLAUDE.md` tag rule: new tags are approved before commit on
      the interactive path, but *deferred* to `curate` on the unattended path via
      `provisional` status and a log record — never silently minted
- [ ] 1.7 Rewrite the `CLAUDE.md` Image-handling claim that "the Phase 2 interview
      is the review/consent point" for figures — true on the interactive path only;
      state that unattended figure judgment is the LLM's, logged and reversible
- [ ] 1.8 Backfill `status: reviewed` into the front-matter of every existing
      `wiki/` knowledge page (summaries, entities, concepts, analyses) —
      front-matter only, no body edits
- [ ] 1.9 Verify the backfill: every knowledge page has exactly one `status:`
      line with a valid value, and `git diff` shows no body changes

## 2. Curate command (the drain — lands before the faucet)

- [ ] 2.1 Add a `## [<date>] curate: <subject>` entry convention to the `log.md`
      section of `CLAUDE.md`, alongside the existing `ingest` and `lint` ops
- [ ] 2.2 Create `.claude/skills/curate/SKILL.md` with the queue-derivation step:
      scan `wiki/` front-matter for `status: provisional`, report queue size and
      oldest-entry age, write nothing by default
- [ ] 2.3 Implement the corpus-relational presentation: for each queued page,
      surface its hub links, overlapping/duplicate existing pages, and pages it
      extends or contradicts — not merely a restatement of the drafted text
- [ ] 2.4 Implement duplicate-hub clustering across the queue and against
      existing hubs (casing, punctuation, name-form, abbreviation, plural
      variants), proposing a canonical page per cluster without merging
- [ ] 2.5 Implement the review verbs: endorse, edit-then-endorse, retag,
      reclassify (with folder re-filing and `index.md` regrouping), merge-hub,
      reject
- [ ] 2.6 Implement merge-hub application: rewrite every inbound `[[wikilink]]`
      to the canonical page, carry over Sources backlinks, delete the variant,
      update `index.md`
- [ ] 2.7 Implement reject application: delete the page, remove its `index.md`
      entry, strip its backlink from every citing hub, delete hubs orphaned by
      the rejection, remove any `wiki/assets/` copy the page had promoted, leave
      `raw/` and `raw/assets/` untouched, no tombstone
- [ ] 2.8 Implement the propose → coach → commit gate: preview all intended
      changes, write nothing without an explicit commit, append exactly one
      `curate` log entry recording endorsements, merges, and rejections with
      reasons
- [ ] 2.9 Add guardrails to the skill: never edit or rename anything under
      `raw/`, never repair structural defects (that is `lint`'s job), leave
      undecided pages `provisional`

## 3. Inbox queue

- [ ] 3.1 Create `inbox.md` at the repo root: a header comment documenting the
      line format (`- [ ]` unprocessed, `- [x]` ingested, `- [!]` parked, URL
      followed by an optional separator and curator note) plus an empty checklist
- [ ] 3.2 Document `inbox.md` in `CLAUDE.md`: its purpose, why it lives at the
      root rather than under `wiki/` (not a knowledge page, not published, not
      linted), and that it is committed mutable working state
- [ ] 3.3 Confirm `inbox.md` is committed and not swept into `.gitignore`, and
      that a site build does not publish it

## 4. Unattended ingest path

- [ ] 4.1 Create `.claude/skills/ingest-inbox/SKILL.md` covering inbox parsing:
      read `- [ ]` entries only, split each into source and optional curator note
- [ ] 4.2 Implement duplicate detection: skip an entry whose URL/path already
      appears as an existing summary's `source:`, writing no `raw/` twin and
      checking the entry off as already ingested
- [ ] 4.3 Implement the per-entry capture step by calling the existing
      `uv run wiki-capture "<source>"` unchanged, parsing its JSON result
- [ ] 4.4 Implement the implausible-capture refusal: detect a thin, cookie-wall,
      paywall, login, or error-page twin, write no `wiki/` pages, park the entry
      with the reason, leave the twin in place
- [ ] 4.5 Implement non-interactive authoring: type, title, tags preferring the
      existing vocabulary, `[[wikilinks]]` to existing hubs, creation of new hubs
      as warranted, and a drafted `## Summary`
- [ ] 4.5a Record every newly-minted tag in that ingest's `wiki/log.md` entry, so
      the tag approval deferred from ingest is visible to `curate`
- [ ] 4.6 Implement drafted `## Why this matters`, seeded by the entry's curator
      note when present and inferred from source-plus-corpus when absent
- [ ] 4.7 Implement autonomous figure handling on the Jina route: judge which
      localized figures carry meaning, distill those into `## Summary`, promote
      only figures prose cannot replace into `wiki/assets/`, record promotions in
      the log entry
- [ ] 4.8 Write `status: provisional` on every page the path creates; write
      `status: provisional` on newly created hubs; leave an existing
      `status: reviewed` hub at `reviewed` when only appending a Sources backlink
- [ ] 4.9 Implement bookkeeping per entry: `index.md` entry, `wiki/log.md` entry
      marked as unattended, and one git commit in the existing `Ingest: <title>`
      style
- [ ] 4.10 Implement inbox writeback: mark each entry `- [x]` on success or
      `- [!]` with date and reason on failure; never delete an entry
- [ ] 4.11 Implement per-entry failure isolation so one failure never aborts the
      run or discards completed work, and emit a per-entry outcome summary
- [ ] 4.12 Implement the end-of-run push: rebase on the remote, push once,
      abort loudly on conflict leaving commits local, never force-push, never
      resolve a content conflict
- [ ] 4.13 Audit the whole skill for interactive branches and remove them — every
      ambiguity must resolve to a documented default or a parked entry, so a
      headless run can never hang on a prompt

## 5. Verification

- [ ] 5.1 Verify idempotence: run against a fully drained inbox and confirm no
      files under `raw/` or `wiki/` are created or modified
- [ ] 5.2 Verify failure isolation with a deliberately broken link alongside two
      good ones: both good entries land, the broken one is parked with a reason
- [ ] 5.3 Verify duplicate skip using a URL already present as an existing
      summary's `source:`
- [ ] 5.4 Exercise the full path manually on a small inbox of 2–3 real links,
      inspecting the resulting diff before allowing the push
- [ ] 5.5 Run `curate` against the resulting provisional queue and exercise each
      verb at least once, including a reject, confirming the `raw/` twin survives
- [ ] 5.6 Run `lint` over the corpus with provisional pages present and confirm it
      reports clean — provisional is not a defect
- [ ] 5.6a Confirm `CLAUDE.md` contains no surviving statement that contradicts the
      unattended path: reread it end to end against the change, since it is binding
      on every operation that reads or writes wiki content
- [ ] 5.7 Build the site and confirm provisional pages publish and `inbox.md` does
      not

## 6. Documentation

- [ ] 6.1 Update the `README.md` Principles list, which still describes ingest as
      inherently interactive, and add the two new commands to the Commands list
      with the capture-cadence / review-cadence split
- [ ] 6.2 Document in `CLAUDE.md` that `lint` audits structure while `curate`
      exercises judgment, and that the two are deliberately orthogonal
- [ ] 6.3 Record the deferred decisions from `design.md` open questions —
      surfacing `status` to site readers, and any per-run batch cap — as
      follow-up notes rather than silently dropping them
