# image-capture Specification

## Purpose

Preserve a source's meaningful figures alongside the raw twin so they can enter
the curated `wiki/` layer, without forcing an up-front decision before anyone has
seen the page. For the web/Jina route, image localization is on by default: a
source's content images are downloaded into the immutable `raw/assets/` layer
with the twin's links rewritten to local copies, while decorative noise is
filtered mechanically. A `--no-images` opt-out suppresses localization for a
source where even filtered figures are unwanted. Human review moves to the Phase
2 author interview, where the LLM presents the localized figures for
review-and-consent, distills the meaningful ones into summary prose, drops the
noise, and lazily promotes only must-see figures to `wiki/assets/` for
publishing.

## Requirements

### Requirement: Image localization defaults on for the web/Jina route

The `file` command SHALL localize a web/Jina source's content images by default,
with no flag required. A `--no-images` opt-out SHALL suppress localization for a
source, leaving the raw twin's original remote image links untouched and
downloading nothing. Selectivity is mechanical: the noise filter is the primary
control, so a page with no content images downloads nothing even with
localization on. The decision is made at the source level, not per individual
image.

#### Scenario: Default web capture localizes content images

- **WHEN** a web URL is filed with no flag
- **THEN** its content images (those passing the filter) are downloaded into
  `raw/assets/<twin-stem>/` and the twin's links are rewritten to the local copies

#### Scenario: --no-images suppresses localization

- **WHEN** a web URL is filed with `--no-images`
- **THEN** the raw twin retains the converter's original remote image links and no
  `raw/assets/` files are written for that source

#### Scenario: A text page downloads nothing by default

- **WHEN** a web URL with no content images (only filtered chrome, or none) is
  filed with no flag
- **THEN** no `raw/assets/` files are written, because the filter removed every
  candidate

### Requirement: Localization report is always available

When localization runs for a web/Jina source, capture SHALL report which images
were kept and which were skipped (with reasons), unconditionally, so the `file`
skill can present the result during the Phase 2 review. The report SHALL be
emitted whether or not any images were kept.

#### Scenario: Report accompanies a default capture

- **WHEN** a web URL is filed with no flag
- **THEN** the capture output includes a kept/skipped image report

#### Scenario: Suppressed localization reports nothing localized

- **WHEN** a web URL is filed with `--no-images`
- **THEN** no localization report of kept images is produced for that source

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

During the Phase 2 author interview, the LLM SHALL present the auto-localized
figures to the user as the review-and-consent step, distill the meaningful ones
into the `## Summary` section as text (description or transcription), and let the
user drop any that are noise. A dropped figure SHALL simply not be surfaced in
`wiki/` — it is neither distilled into prose nor promoted to `wiki/assets/` — while
its localized bytes under `raw/assets/<twin-stem>/` remain (immutable); cleanup of
unreferenced raw assets is deferred to the future `lint` command. This extends the
dual-voice summary without changing its section structure: figure descriptions
live within `## Summary`, and `## Why this matters` remains the user's commentary.

#### Scenario: Localized figures are reviewed in the interview

- **WHEN** a source was captured with images localized
- **THEN** the LLM presents the localized figures during Phase 2 so the user can
  decide which to keep

#### Scenario: Meaningful figure becomes text

- **WHEN** a source's localized figures include one that carries meaning
- **THEN** the committed summary's `## Summary` section describes or transcribes
  that figure in prose

#### Scenario: Noise figure is dropped without surfacing

- **WHEN** the user marks a localized figure as noise during the review
- **THEN** it is not distilled into the summary nor promoted to `wiki/assets/`,
  and its `raw/assets/` bytes are left in place

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
behavior. Default-on localization and the `--no-images` opt-out affect only the
web/Jina route.

#### Scenario: PDF capture is unaffected

- **WHEN** a PDF is filed, with or without `--no-images`
- **THEN** image localization into `raw/assets/` is not performed by this
  capability and Docling's existing behavior is unchanged
