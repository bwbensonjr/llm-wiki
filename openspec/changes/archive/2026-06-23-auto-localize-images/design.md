## Context

The shipped `image-capture` capability makes localization opt-in: `wiki-capture
<url> --images` downloads content figures into `raw/assets/<twin-stem>/` and
rewrites the twin's links before the single twin write. Without the flag, capture
writes the twin with the converter's remote links and downloads nothing. The flag
must be chosen before the page's content is visible, so figures are lost whenever
it is forgotten — the friction the user hit.

Three properties cannot all hold for a "suggest before downloading" flow:
look-before-write, write-once, and single-fetch. The user chose **auto-localize,
then review**: keep write-once and single-fetch, and move the human's
review/consent into the Phase 2 interview rather than a pre-download prompt.

## Goals / Non-Goals

**Goals:**
- Remove the up-front flag; web pages "just work."
- Preserve write-once, single-fetch, and `raw/` immutability exactly as today.
- Make the Phase 2 interview the explicit review/consent point for localized
  figures, including dropping noise.

**Non-Goals:**
- A pre-download probe/confirm step (the rejected look-before-write option).
- Deleting unreferenced raw assets at ingest time (a future `lint` concern).
- Any change to the filter, storage layout, lazy `wiki/assets/` promotion, or the
  PDF/MarkItDown routes.

## Decisions

### Decision: Flip the default; replace `--images` with `--no-images`
`capture(..., localize_images=True)` becomes the default; localization still only
runs for the Jina route, so PDFs/MarkItDown are untouched. The CLI drops
`--images` and adds `--no-images` (sets `localize_images=False`).
- *Why:* the mechanical filter is already the selectivity mechanism — a text page
  yields zero content images and downloads nothing, so default-on is safe. The
  consent the flag used to provide moves to Phase 2.
- *BREAKING:* `--images` no longer exists. Acceptable: the flag shipped in the
  same session, has no external users, and the migration is documented in the
  delta.
- *Alternative considered:* keep `--images` as an accepted no-op for
  back-compat — rejected as needless cruft in a single-user repo.

### Decision: The Phase 2 interview is the review/consent point
The `file` skill, in Phase 2, presents the localized figures (from the always-on
report), distills the meaningful ones into `## Summary`, and lets the user drop
the rest. A dropped figure is simply not surfaced in `wiki/` (not distilled, not
promoted); its `raw/assets/` bytes remain immutable.
- *Why:* preserves write-once and immutability — nothing is deleted or rewritten
  after the twin is authored. The human still has full control over what reaches
  the curated layer, just after the cheap mechanical download rather than before.
- *Trade-off:* filtered bytes are committed to `raw/assets/` even if later judged
  noise. Bounded by the filter; unreferenced assets are a `lint` matter.

### Decision: Report is unconditional for the web route
Because there is no flag, the `images` report must always accompany a web capture
so the skill knows what to present. `capture()` already returns the report; the
CLI prints it whenever localization ran.

## Risks / Trade-offs

- **A large decorative image passes the filter and is downloaded uninvited** →
  the user drops it in Phase 2; it stays in `raw/assets/` but never reaches
  `wiki/`. Filter thresholds remain tunable; `lint` can later flag unreferenced
  assets.
- **`--no-images` forgotten on a genuinely image-heavy-but-worthless page** →
  wasted bytes only; no correctness impact, and the review catches it before
  anything publishes.
- **Existing tests assume opt-in** → they are updated as part of this change
  (default now localizes; a new test covers `--no-images`).

## Migration Plan

Additive-but-breaking only at the CLI flag. No data migration: existing twins are
untouched (immutable). Rollback = restore the `--images` flag and the opt-in
default. Update `CLAUDE.md` and the `file` skill so the convention and workflow
match the new default.

## Open Questions

- Whether `lint` should eventually delete or just flag `raw/assets/` files that no
  summary references — out of scope here, noted for the `lint` capability.
