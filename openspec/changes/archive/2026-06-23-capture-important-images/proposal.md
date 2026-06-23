## Why

The Jina Reader route captures HTML pages as Markdown that references images by
remote URL only; it never downloads the bytes. Many of those URLs are signed,
expiring links (e.g. GitHub `private-user-images` carry a JWT `exp`), so they rot
— some are already dead in twins we have ingested — and even live URLs sit inline
where the LLM cannot read them in a single pass. For sources where a figure
actually carries meaning (a diagram, a chart), that knowledge is lost at capture.
Karpathy's gist calls this out directly and recommends downloading images locally
to a fixed assets folder, while noting image handling should stay optional and
modular for a text-dominant corpus.

## What Changes

- Add an **opt-in** image-localization path to the `file` capture phase for the
  web/Jina route. Default behavior is unchanged: no flag, no downloads.
- When enabled for a source, Phase 1 downloads that source's referenced images
  into `raw/assets/<twin-stem>/` and rewrites the twin's image links to point at
  the local copies, so the immutable raw twin becomes self-contained and offline.
- Apply mechanical noise filtering (skip avatar/tiny/decorative images by URL
  pattern and size) so a flagged source still does not drag in junk.
- In the Phase 2 interview, the LLM **views the localized figures and distills
  the meaningful ones into the summary prose** (`## Summary`), so a figure's
  knowledge survives into `wiki/` as text — consistent with wiki being a
  compiled distillation of raw, not a copy.
- Add **lazy promotion** to `wiki/assets/`: only when a figure must actually be
  *seen* on the published Quartz site does a curated copy move into `wiki/assets/`
  and get embedded in the summary. The directory is created on first use, not
  speculatively.
- Scope is the web/Jina (HTML) route only. PDF (Docling) and other (MarkItDown)
  image handling is explicitly out of scope for this change.

## Capabilities

### New Capabilities
- `image-capture`: Optional, source-level localization of referenced images into
  the immutable `raw/` layer during capture, distillation of meaningful figures
  into summary prose during the author interview, and lazy promotion of must-see
  figures into the published `wiki/` layer.

### Modified Capabilities
<!-- None. This change is purely additive: existing resource-ingestion
     requirements (converter routing, two-phase file command, two-layer storage,
     dual-voice summaries) remain true as written. image-capture layers new,
     opt-in behavior on top without rewording any of them. -->

## Impact

- **Code**: `wiki_ingest/convert.py` (Jina route gains an optional localize step
  before the raw twin is written), a new image-localization helper module, the
  `file` skill instructions (Phase 1 flag, Phase 2 figure-distillation and
  promotion steps), and `wiki_ingest/cli.py` (capture flag).
- **Storage**: new `raw/assets/<twin-stem>/` directories (immutable, committed);
  new `wiki/assets/` directory created lazily (committed, published).
- **Publishing**: figures promoted to `wiki/assets/` are served by Quartz's
  existing `Plugin.Assets()`; nothing under `raw/` is published.
- **Conventions**: `CLAUDE.md` gains an assets/image-handling note; no change to
  page taxonomy or front-matter schema.
- **Dependencies**: image download reuses the existing `requests` session; no new
  runtime dependency.
