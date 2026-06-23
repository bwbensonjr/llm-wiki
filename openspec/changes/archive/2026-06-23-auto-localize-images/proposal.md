## Why

The `image-capture` capability requires the user to pass `--images` up front to
keep a source's figures. That forces a decision before anyone has seen the
page's content, so meaningful figures are silently lost whenever the flag is
forgotten. The capture already converts the page in memory and already has a
mechanical filter that separates content figures from avatars/thumbnails — so it
can simply localize the content figures by default and let the Phase 2 interview
be where the human reviews and decides what to keep. This removes the up-front
flag and makes image handling "just work" for web pages.

## What Changes

- **BREAKING (CLI):** Replace the opt-in `--images` flag with **default-on**
  localization for the web/Jina route, plus a `--no-images` opt-out for the rare
  text page where even filtered figures are unwanted.
- The mechanical avatar/thumbnail/size filter becomes the **primary selectivity
  mechanism**: a text page yields no content images and downloads nothing, so the
  default is safe.
- Capture always reports what it localized (the `images` report is no longer
  gated behind a flag) so the `file` skill can surface it.
- The Phase 2 interview becomes the **review-and-consent point**: the LLM
  presents the localized figures, distills the meaningful ones into the summary
  prose, and the user can drop any that are noise. Dropped figures simply are not
  surfaced in `wiki/` — the raw localization stands (immutable), and unreferenced
  raw assets are a future `lint` concern, not ingest's.
- Single fetch, write-once, and `raw/` immutability are all preserved — only the
  default and the consent point move.

## Capabilities

### New Capabilities
<!-- None. -->

### Modified Capabilities
- `image-capture`: localization flips from opt-in (`--images`) to default-on for
  the web/Jina route with a `--no-images` opt-out; the Phase 2 interview becomes
  the explicit review/consent step for the auto-localized figures.

## Impact

- **Code**: `wiki_ingest/convert.py` (`capture()` default for `localize_images`
  flips to on, scoped to the Jina route as today), `wiki_ingest/cli.py`
  (`--images` → `--no-images`).
- **Skill**: `.claude/skills/file/SKILL.md` — Phase 1 no longer instructs adding
  a flag; Phase 2 gains the "present localized figures, distill or drop" review
  step.
- **Conventions**: `CLAUDE.md` "Image handling" section reworded from opt-in to
  default-on + `--no-images`, with the review/consent point in Phase 2.
- **Tests**: update the existing default-localizes-nothing / flagged-capture
  tests to the new default; add a `--no-images` suppression test.
- No change to storage layout (`raw/assets/<twin-stem>/`, lazy `wiki/assets/`),
  the filter, or the all-or-nothing guarantee.
