## Why

Ingest is gated on a live interview: every source requires the curator present to
approve a classification, approve tags, review figures, and dictate "Why this
matters." That gate was justified when LLM proposals needed checking — but in
practice the proposals have been good, and the gate is now the sole reason the
wiki grows one source per sitting instead of one batch per day. Meanwhile the
gate conflates five different jobs (consent, taxonomy, tag vocabulary, figure
judgment, curatorial voice), only one of which is irreducibly human, and it
forces all five to happen at the same moment: the moment a link is captured.

This change separates **capture cadence** from **review cadence**. Links are
ingested unattended and land as fully-formed but explicitly *provisional* pages;
the curator reviews accumulated provisional pages later, offline, in a batch —
endorsing, correcting, or rejecting. The human judgment is preserved and moved,
not removed.

## What Changes

- **A committed root `inbox.md`** becomes the source queue: a checklist of links,
  each optionally carrying a trailing curator note. The curator appends to it
  from anywhere; the batch ingest drains it, checking off what it ingested and
  annotating what failed.
- **A new unattended ingest path** runs Phase 1 capture unchanged, then authors
  the wiki layer without an interview: it classifies, titles, tags, links to
  existing hubs, creates new hubs as needed, distills and promotes figures on its
  own judgment, and drafts `## Why this matters` — seeded by the inbox note when
  one was given. Each link is isolated: one failure does not abort the batch.
- **A `status:` front-matter field** (`provisional` | `reviewed`) marks every
  knowledge page's review state. Unattended writes are `provisional`;
  interactive `file` writes and curator-endorsed pages are `reviewed`. The
  review queue is *derived* — the set of pages carrying `status: provisional` —
  not a separate maintained list that can drift from reality.
- **Autonomous commit and push.** The batch commits per source in the existing
  `Ingest: <title>` style and pushes to `main`, so provisional pages publish to
  the live site with no human contact. `status: provisional` is therefore a
  reader-facing honesty signal, not just internal bookkeeping.
- **A new `curate` command** drains the provisional queue through the
  established propose → coach → commit interview, with the verbs review actually
  needs: endorse, edit-then-endorse, retag, reclassify, merge duplicate hubs, and
  **reject** (delete the page, unlink it, log it — the immutable `raw/` twin
  stays).
- **BREAKING (conceptually, not mechanically):** `## Why this matters` changes
  meaning from "prose the curator wrote" to "significance the curator stands
  behind." Existing pages remain valid — they are all curator-authored and
  become `status: reviewed` — but the requirement that the LLM must solicit the
  commentary before committing no longer holds on the unattended path.

Explicitly **not** changing: `raw/` immutability, converter routing, the page
taxonomy, the mechanical image-localization filter, `lint`, and the publish
pipeline. Provisional pages publish through Quartz normally and unfiltered — this
is an information source, not an operational system needing staged release.

`lint` in particular is left alone deliberately: a provisional page is *not* a
defect, and reporting it as one would make the steady state of an auto-ingesting
wiki permanently "dirty," destroying the clean/dirty signal that makes `lint`
worth running. `lint` audits structure; `curate` exercises judgment. They stay
orthogonal.

## Capabilities

### New Capabilities

- `unattended-ingestion`: the `inbox.md` source queue and the non-interactive
  authoring path — provisional-status writes, per-link failure isolation,
  already-ingested duplicate detection, inbox-note seeding of drafted
  commentary, and autonomous commit/push.
- `corpus-curation`: the `curate` command — deriving the provisional queue from
  front-matter, presenting recent additions for review, the endorse / edit /
  retag / reclassify / merge-hub / reject verbs, duplicate-hub clustering across
  a batch, and the curator-gated commit that flips pages to `reviewed`.

### Modified Capabilities

- `resource-ingestion`: three requirements change. **Dual-voice summary pages**
  moves from authorship-gated ("the user's own commentary") to endorsement-gated —
  `## Why this matters` may be LLM-drafted while a page is `provisional`, and
  becomes curator-endorsed on review. **Tag vocabulary consistency at ingest**
  currently requires every newly-minted tag to be approved *before commit*, which
  no unattended path can satisfy; approval becomes **deferred** rather than
  skipped — the run logs every tag it minted and `curate` approves or redirects it
  at review. **Wiki page taxonomy** gains the `status:` field. The interactive
  `file` command's Phase 2 interview is otherwise unchanged and still writes
  `status: reviewed` directly.

  Both relaxed requirements share one shape: an approval gate with no approver
  present. Each is converted to a *deferred* approval backed by `provisional`
  status and a log record, never to a silently dropped one.
- `image-capture`: the **Phase 2 figure review** and **Lazy promotion**
  requirements currently require explicit user approval to distill a figure into
  prose or promote its bytes to `wiki/assets/`. On the unattended path that
  judgment passes to the LLM, with the decision recorded for review; the
  mechanical skip filter and `raw/assets/` immutability are untouched.

## Impact

- **`CLAUDE.md` — binding conventions, not documentation.** Its own header makes
  it authoritative for any operation that reads or writes wiki content, so the
  passages this change contradicts must be rewritten as part of the change, not
  after it. Specifically: the opening framing of who does what ("the human curates
  sources and asks questions; the LLM summarizes, cross-references, files, and
  keeps the books" — the LLM now also judges, and the human reviews afterward); the
  four front-matter YAML blocks, which gain `status:`; the definition of
  `## Why this matters` as "the curator's commentary"; the tag rule "surface any
  genuinely new tag explicitly for the user to approve"; the Image-handling claim
  that "the Phase 2 interview is the review/consent point" for figures, now true
  only on the interactive path; and the `log.md` op vocabulary, which gains
  `curate`. A new section documents `inbox.md` and the lint/curate split.
- **`README.md`** — the Principles list still describes ingest as inherently
  interactive; it and the Commands list need the two new commands and the
  capture-cadence / review-cadence split.
- **New content file:** `inbox.md` at the repo root — committed, mutable working
  state (deliberately not under `wiki/`, so Quartz does not publish it and
  `lint` does not read it as an untyped knowledge page).
- **New skills:** the unattended ingest command and `curate`, alongside the
  existing `file`, `query`, and `lint` skills in `.claude/skills/`. Naming note:
  `review` collides with a built-in Claude Code PR-review skill, hence `curate`.
- **`wiki_ingest/` CLI:** unchanged for single-source capture. Batch iteration,
  inbox parsing, and duplicate detection are new surface — a decision for
  `design.md` on whether they live in the Python CLI or the skill.
- **Templates:** `templates/summary.md`, `entity.md`, `concept.md` gain
  `status:`. Existing pages need a one-time backfill to `status: reviewed`.
- **Published site:** provisional pages go live; the `status:` field should be
  visible to readers so machine-judged pages are distinguishable from endorsed
  ones.
- **Git:** the batch commits and pushes to `main`, triggering the Pages deploy
  via `.github/workflows/publish.yml`. This is the only step that reaches
  outside the machine.
- **`wiki/log.md`:** gains unattended-ingest entries and `curate` entries,
  including rejections — for a rejected page the log becomes the only surviving
  record in `wiki/`.
