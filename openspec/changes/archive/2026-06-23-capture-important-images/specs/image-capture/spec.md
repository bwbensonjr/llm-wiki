## ADDED Requirements

### Requirement: Image localization is opt-in per source

The `file` command SHALL NOT localize images by default. Image localization
SHALL be requested explicitly at capture time (a Phase 1 flag). When the flag is
absent, capture behaves exactly as before: the raw twin retains the converter's
original remote image links and no image bytes are downloaded. The opt-in is
made at the source level — the human decides a given source has figures worth
keeping — not per individual image.

#### Scenario: Default capture localizes nothing

- **WHEN** a web URL is filed without the image flag
- **THEN** the raw twin contains the converter's original remote image links and
  no `raw/assets/` files are written for that source

#### Scenario: Flag enables localization for the source

- **WHEN** a web URL is filed with the image flag set
- **THEN** that source's eligible images are downloaded and the raw twin links
  are rewritten to the local copies

### Requirement: Localized images live immutably under raw/assets

When localization is enabled, Phase 1 SHALL download the source's eligible
images into `raw/assets/<twin-stem>/`, where `<twin-stem>` is the raw twin's
filename without extension (e.g. twin `raw/2026-06-23-foo.md` →
`raw/assets/2026-06-23-foo/`). These files are part of the immutable `raw/`
layer: once written they SHALL NOT be edited or renamed by any later operation.
The raw twin's image links SHALL be rewritten, before the twin is written, to
relative paths pointing at the downloaded copies, so the twin is self-contained
and viewable offline.

#### Scenario: Assets folder mirrors the twin stem

- **WHEN** localization writes images for twin `raw/<date>-<slug>.md`
- **THEN** the bytes are written under `raw/assets/<date>-<slug>/` and the twin's
  image links reference those relative paths

#### Scenario: Localized assets are immutable

- **WHEN** a later operation (authoring, lint, re-ingest) runs over a source
  whose images were localized
- **THEN** the existing files under `raw/assets/<twin-stem>/` are not edited or
  renamed

#### Scenario: Link rewrite happens within the single capture write

- **WHEN** images are localized during Phase 1
- **THEN** the raw twin is written once with the rewritten links, not edited
  after the fact

### Requirement: Mechanical noise filtering of decorative images

When localizing, the `file` command SHALL skip images that are mechanically
identifiable as decorative or non-content — including avatar/profile-image URL
patterns and images below a size threshold — so that even a flagged source does
not pull in junk. Filtering SHALL be mechanical (URL/heuristic based) and SHALL
NOT require LLM judgment, preserving Phase 1 as a non-interactive step.

#### Scenario: Avatars are skipped

- **WHEN** a flagged source references commenter avatar images
  (e.g. `avatars.githubusercontent.com`)
- **THEN** those images are not downloaded and the twin's link to them is left as
  the original remote URL or dropped per the filter rule

#### Scenario: Content figures are kept

- **WHEN** a flagged source references a content figure that passes the filter
- **THEN** that image is downloaded into `raw/assets/<twin-stem>/`

### Requirement: Conversion failure still writes nothing

Image localization SHALL preserve the all-or-nothing capture guarantee. If the
core conversion fails, no twin and no assets are written. A failure to download
an individual eligible image SHALL NOT abort the capture; the twin is still
written, the failed image's link is left as its original remote URL, and the
skip is reported to the user.

#### Scenario: Core conversion failure leaves no assets

- **WHEN** Phase 1 conversion of the source fails
- **THEN** neither the raw twin nor any `raw/assets/` files are written

#### Scenario: A single image download failure is tolerated

- **WHEN** localization is enabled and one eligible image cannot be downloaded
- **THEN** the raw twin is still written, that image's link remains the original
  remote URL, and the user is told which image was skipped

### Requirement: Figures are distilled into summary prose

During the Phase 2 author interview, the LLM SHALL view the localized figures and
distill the meaningful ones into the `## Summary` section as text (description or
transcription), so a figure's knowledge enters the `wiki/` layer as prose. This
extends the existing dual-voice summary without changing its section structure:
figure descriptions live within `## Summary`, and `## Why this matters` remains
the user's commentary.

#### Scenario: Meaningful figure becomes text

- **WHEN** a source's localized figures include one that carries meaning
- **THEN** the committed summary's `## Summary` section describes or transcribes
  that figure in prose

#### Scenario: Summary structure is unchanged

- **WHEN** a summary is committed for a source with localized images
- **THEN** the page still has exactly the `## Summary` and `## Why this matters`
  sections, with figure descriptions contained within `## Summary`

### Requirement: Lazy promotion of must-see figures to wiki/assets

A localized figure SHALL be copied into `wiki/assets/` only when it must be
*seen* on the published site (prose cannot substitute) and the user approves
during the interview. The `wiki/assets/` directory SHALL be created on first such
promotion, not speculatively. The promoted copy SHALL be embedded in the summary
via an Obsidian-compatible image reference; the original under
`raw/assets/<twin-stem>/` remains the immutable source of truth.

#### Scenario: Figure is promoted on demand

- **WHEN** the user approves displaying a figure on the published site
- **THEN** a copy is placed under `wiki/assets/` and embedded in the summary,
  while the raw original is retained

#### Scenario: No promotion means no wiki/assets churn

- **WHEN** a source's figures are localized but none need to be displayed
- **THEN** no files are written under `wiki/assets/` and the directory is not
  created for that source

#### Scenario: Promoted figures publish via Quartz

- **WHEN** the site is built after a figure is promoted to `wiki/assets/`
- **THEN** the figure is served from the built site and no `raw/` content is
  published

### Requirement: Scope limited to the web/Jina route

This capability SHALL apply to the web/Jina (HTML) conversion route only. The PDF
(Docling) and other-file (MarkItDown) routes SHALL retain their current image
behavior and are out of scope for this change.

#### Scenario: PDF capture is unaffected

- **WHEN** a PDF is filed, with or without the image flag
- **THEN** image localization into `raw/assets/` is not performed by this
  capability and Docling's existing behavior is unchanged
