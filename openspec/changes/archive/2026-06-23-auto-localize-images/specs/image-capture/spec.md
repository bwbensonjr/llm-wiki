## REMOVED Requirements

### Requirement: Image localization is opt-in per source

**Reason**: Forcing an up-front `--images` decision before anyone has seen the
page loses figures whenever the flag is forgotten. The mechanical filter already
separates content figures from chrome, so localization can default on and the
human review can move to the Phase 2 interview.

**Migration**: Localization is now on by default for the web/Jina route. Pass
`--no-images` to `wiki-capture` to suppress it for a source where even filtered
figures are unwanted. See the new requirement "Image localization defaults on
for the web/Jina route."

## ADDED Requirements

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

## MODIFIED Requirements

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

### Requirement: Scope limited to the web/Jina route

This capability SHALL apply to the web/Jina (HTML) conversion route only. The PDF
(Docling) and other-file (MarkItDown) routes SHALL retain their current image
behavior. Default-on localization and the `--no-images` opt-out affect only the
web/Jina route.

#### Scenario: PDF capture is unaffected

- **WHEN** a PDF is filed, with or without `--no-images`
- **THEN** image localization into `raw/assets/` is not performed by this
  capability and Docling's existing behavior is unchanged
