## 1. Image localization helper (`wiki_ingest/images.py`)

- [x] 1.1 Add a function that parses Markdown for image references
  (`![alt](src)`, including the inner image of wrapped `[![alt](src)](link)`),
  returning each image's `src` and span for rewriting.
- [x] 1.2 Add a mechanical noise filter: skip avatar/decorative URL patterns
  (e.g. `avatars.githubusercontent.com`, `?s=<small>` thumbnails) and, after
  download, images below a size threshold.
- [x] 1.3 Add a downloader that fetches an eligible image via the shared
  `requests` session, derives a stable local filename, and writes it under a
  given assets directory; tolerate per-image failure by signalling skip rather
  than raising.
- [x] 1.4 Add a `localize(markdown, assets_dir, rel_prefix, session)` orchestrator
  that downloads kept images, rewrites their `src` to relative paths, leaves
  failed/filtered images as their original remote URL, and returns the rewritten
  Markdown plus a report of kept/skipped images.

## 2. Wire localization into capture (`wiki_ingest/convert.py`)

- [x] 2.1 Add a `localize_images=False` parameter to `capture()`; thread the
  shared `session` through to the localizer.
- [x] 2.2 After `_unique_path` resolves the twin path, when `localize_images` is
  set and the route is Jina, run `localize` with `assets_dir =
  raw_dir/"assets"/<twin-stem>` and `rel_prefix = "assets/<twin-stem>"` before
  writing the twin; write the twin once with the rewritten Markdown.
- [x] 2.3 Ensure the all-or-nothing guarantee holds: core conversion failure
  writes neither twin nor assets; only create the assets directory when at least
  one image is kept.
- [x] 2.4 Surface the kept/skipped image report on `CaptureResult` so the CLI can
  print it.

## 3. CLI flag (`wiki_ingest/cli.py`)

- [x] 3.1 Add a `--images` flag (default off) and pass `localize_images` into
  `capture()`.
- [x] 3.2 Include the kept/skipped image report in the JSON printed to stdout.

## 4. `file` skill instructions

- [x] 4.1 Document the Phase 1 `--images` opt-in and when to use it (sources whose
  figures carry meaning).
- [x] 4.2 Add a Phase 2 step: `Read` the localized figures from
  `raw/assets/<twin-stem>/` and distill meaningful ones into `## Summary` prose,
  keeping the dual-voice section structure unchanged.
- [x] 4.3 Add a Phase 2 lazy-promotion step: on user approval, copy a must-see
  figure into `wiki/assets/` (creating it on first use) and embed it in the
  summary via Obsidian image syntax, leaving the raw original intact.

## 5. Conventions and docs

- [x] 5.1 Add an assets/image-handling note to `CLAUDE.md`: `raw/assets/<twin-stem>/`
  (immutable, bytes), figures distilled to prose by default, `wiki/assets/`
  (curated, published, lazy), scope = web/Jina route only.
- [x] 5.2 Confirm `.gitignore` does not exclude `raw/assets/` or `wiki/assets/`
  (they are content and must be committed).

## 6. Tests

- [x] 6.1 Test default capture localizes nothing (no `--images`, twin keeps remote
  links, no `raw/assets/` written).
- [x] 6.2 Test flagged capture downloads content images into
  `raw/assets/<twin-stem>/` and rewrites links to relative paths.
- [x] 6.3 Test the noise filter skips avatars/thumbnails and keeps content figures.
- [x] 6.4 Test a single image download failure leaves that link remote, still
  writes the twin, and reports the skip; test core conversion failure writes
  nothing (twin and assets).
- [x] 6.5 Test the assets folder stem matches the twin stem, including the
  `_unique_path` `-2` suffix collision case.

## 7. Validate

- [x] 7.1 Run `mise exec -- openspec validate capture-important-images --strict`
  and fix any issues.
