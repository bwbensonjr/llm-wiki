## 1. Flip the default in capture

- [x] 1.1 Change `capture()` in `wiki_ingest/convert.py` so `localize_images`
  defaults to `True`; localization still runs only for the Jina route, so PDF/
  MarkItDown captures are unaffected.
- [x] 1.2 Confirm the `images` report is returned on `CaptureResult` whenever
  localization runs (no flag gating).

## 2. Replace the CLI flag

- [x] 2.1 In `wiki_ingest/cli.py`, remove `--images` and add `--no-images`
  (`action="store_true"`), passing `localize_images=not args.no_images`.
- [x] 2.2 Ensure the kept/skipped report still prints in the stdout JSON whenever
  localization ran.

## 3. Update the `file` skill

- [x] 3.1 Phase 1: remove the "add `--images` when figures carry meaning"
  guidance; state that web pages localize content images automatically and
  `--no-images` skips it (rare).
- [x] 3.2 Phase 2: make the figure step an explicit review — present the
  localized figures, distill the meaningful ones into `## Summary`, and let the
  user drop noise (dropped figures are not distilled or promoted; raw bytes
  remain).

## 4. Update conventions

- [x] 4.1 Reword the `CLAUDE.md` "Image handling" section from opt-in (`--images`)
  to default-on for the web/Jina route with a `--no-images` opt-out, and name the
  Phase 2 interview as the review/consent point.

## 5. Tests

- [x] 5.1 Update the prior "default capture localizes nothing" test to assert the
  new default localizes content images for a web source with no flag.
- [x] 5.2 Update the prior flagged-capture test to drive the default path (no
  flag) rather than `localize_images=True`.
- [x] 5.3 Add a `--no-images` / `localize_images=False` test: twin keeps remote
  links, no `raw/assets/` written.
- [x] 5.4 Confirm the noise-filter, download-failure, and stem-collision tests
  still pass under the new default (adjust call sites as needed).

## 6. Validate

- [x] 6.1 Run the test suite (`uv run --group dev pytest`) green.
- [x] 6.2 Run `mise exec -- openspec validate auto-localize-images --strict` and
  fix any issues.
