## Context

`wiki_ingest/convert.py` routes web URLs to Jina Reader (`_convert_jina`), which
returns Markdown with images referenced as remote URLs (often wrapped as
`[![Image N: alt](img-src)](link)`). The returned text is written verbatim into
the immutable raw twin at `raw/<date>-<slug>.md` by `capture()`. No image bytes
are stored. Many remote URLs are signed and expiring (GitHub `private-user-images`
JWTs), so links rot, and inline image Markdown is unreadable by the LLM in a
single pass.

Hard constraints from `CLAUDE.md` and the `resource-ingestion` spec:

- `raw/` is immutable and converter-authored; a twin once written is never edited.
- Capture is all-or-nothing: on conversion failure, write nothing.
- Phase 1 (capture) is mechanical and non-interactive; Phase 2 (author) is the
  interview where judgment and `wiki/` writes happen.
- Quartz publishes `--directory wiki` only, so nothing under `raw/` can render on
  the site; the existing `Plugin.Assets()` already serves files under `wiki/`.

## Goals / Non-Goals

**Goals:**
- Preserve meaningful figures at capture before their URLs expire, as immutable
  raw content.
- Keep the raw twin self-contained (local relative links) and offline-viewable.
- Let a figure's *knowledge* reach `wiki/` as prose; let its *bytes* reach the
  published site only when it must be seen.
- Zero change to default behavior — the feature is opt-in.

**Non-Goals:**
- PDF (Docling) / MarkItDown image handling — out of scope.
- Per-image LLM judgment during Phase 1 (would break the mechanical-capture rule).
- OCR, image-only-PDF pipelines, embedding/vector retrieval (Loremaester
  territory).
- Auto-detecting which sources have meaningful figures — the human opts in.

## Decisions

### Decision: Source-level opt-in flag, not per-image or auto-detect
Localization is requested with a Phase 1 flag (`wiki-capture <url> --images`,
threaded through `capture(..., localize_images=False)`). Deciding *which sources*
have figures worth keeping is a human judgment made at invocation; within a
flagged source, download is mechanical.
- *Why:* Phase 1 must stay mechanical and non-interactive. Per-image "is this
  meaningful?" is judgment and belongs in Phase 2. Auto-detection is unreliable
  and would silently pull bytes on every ingest.
- *Alternative considered:* download-all-always with filtering — rejected; pulls
  noise on a text-dominant corpus and changes default behavior. Interview-time
  decision — rejected; bytes must be grabbed before expiring URLs die, which is
  Phase 1.

### Decision: Localize in `capture()` after the twin path is resolved
The twin stem (`<date>-<slug>`, possibly `-2` suffixed by `_unique_path`) is only
known inside `capture()`. So a new `localize` step runs there: after
`_unique_path` resolves the twin path, parse the in-memory Markdown, download
eligible images into `raw/assets/<twin-stem>/`, rewrite the image `src` to the
relative path `assets/<twin-stem>/<file>`, then write the twin once. A new helper
module (`wiki_ingest/images.py`) owns parsing, filtering, downloading, and link
rewriting; `convert.py` orchestrates.
- *Why:* keeps the rewrite inside the single capture write (no edit-after-write,
  honoring immutability), and keys assets to the same collision-resistant stem as
  the twin.
- *Alternative considered:* rewrite inside `_convert_jina` — rejected; the stem
  isn't known there and Jina stays a pure fetch.

### Decision: Mechanical noise filter (avatars + size)
Skip images whose URL matches known avatar/decorative patterns (e.g.
`avatars.githubusercontent.com`, query `?s=<small>` thumbnails) and images whose
downloaded byte size is below a threshold. Filtering is pure heuristic, no LLM.
- *Why:* even a flagged gist/thread is full of avatars; this keeps `raw/assets/`
  to content figures without judgment.
- *Trade-off:* heuristics may occasionally skip a small real figure or keep a
  large decorative one; acceptable and tunable. Skips are reported.

### Decision: Per-image download failure is non-fatal; core conversion failure is fatal
The all-or-nothing guarantee applies to the *conversion*. Within a flagged
source, a single image that 404s/times out leaves its original remote link in the
twin and is reported, rather than aborting an otherwise-good capture.
- *Why:* one dead image (the exact rot we are fighting) must not block capturing
  the text and the other figures.

### Decision: wiki/ gets prose by default; bytes only on lazy promotion
Phase 2 interview: the LLM `Read`s the localized figures and distills meaningful
ones into `## Summary` prose. Only when prose cannot substitute and the user
approves does a curated copy move to `wiki/assets/` (created on first use),
embedded via Obsidian image syntax. Raw original stays the source of truth.
- *Why:* mirrors the wiki-is-a-distillation-of-raw philosophy; avoids publishing
  noise; keeps `wiki/assets/` small and curated.
- *Alternative considered:* always copy figures to `wiki/assets/` — rejected;
  duplicates bytes and publishes avatars/screenshots that carry no meaning.

## Risks / Trade-offs

- **Noise filter misclassifies an image** → heuristics are conservative and skips
  are logged; the user can re-file or adjust. Raw original is recoverable while
  the URL lives.
- **Two-phase purity vs. "selective"** → resolved by making selectivity
  source-level (Phase 1 flag) and mechanical within a source; figure *meaning* is
  assessed in Phase 2. No LLM judgment leaks into capture.
- **Raw twin immutability** → the link rewrite happens before the single write, so
  no twin is edited after the fact; `raw/assets/` files are write-once.
- **Storage growth in git** → assets are committed (they are content/source of
  truth). Opt-in + filtering keeps volume bounded; revisit if it grows.
- **Wrapped image markdown** (`[![alt](img)](link)`) → the rewriter targets the
  inner image `src` only and leaves the wrapping link, so layout is preserved.

## Migration Plan

Purely additive and opt-in; no migration of existing twins. Existing raw twins
keep their remote links. Rollback = stop passing `--images`; the helper module
and flag can remain dormant. `CLAUDE.md` gains a short assets note so the
convention is documented for future ingests.

## Open Questions

- Exact size threshold and the avatar URL pattern set — start conservative
  (skip `avatars.*` and `?s=` thumbnails, keep everything else above ~5 KB) and
  tune from real ingests.
- Whether to also rewrite the wrapping link target to the local copy — default
  no (leave the external full-res link intact); revisit if offline-completeness
  is wanted.
