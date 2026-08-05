## MODIFIED Requirements

### Requirement: Figures are distilled into summary prose

During the Phase 2 author interview, the LLM SHALL present the auto-localized
figures to the user as the review-and-consent step, distill the meaningful ones
into the `## Summary` section as text (description or transcription), and let the
user drop any that are noise. On the **unattended ingest path there is no
interview**, so the LLM SHALL exercise that judgment itself: it decides which
localized figures carry meaning, distills those into `## Summary` as text, and
drops the rest. A dropped figure SHALL simply not be surfaced in `wiki/` — it is
neither distilled into prose nor promoted to `wiki/assets/` — while its localized
bytes under `raw/assets/<twin-stem>/` remain (immutable); cleanup of unreferenced
raw assets is deferred to the `lint` command. A page whose figure decisions were
made unattended carries `status: provisional`, so those decisions are reviewable
and reversible via `curate`. This extends the dual-voice summary without changing
its section structure: figure descriptions live within `## Summary`, and
`## Why this matters` holds the resource's significance to the curator.

#### Scenario: Localized figures are reviewed in the interview

- **WHEN** a source was captured with images localized on the interactive path
- **THEN** the LLM presents the localized figures during Phase 2 so the user can
  decide which to keep

#### Scenario: Figure judgment is autonomous when unattended

- **WHEN** a source captured with localized images is authored on the unattended
  path
- **THEN** the LLM decides without prompting which figures carry meaning, distills
  those into `## Summary`, and drops the rest

#### Scenario: Meaningful figure becomes text

- **WHEN** a source's localized figures include one that carries meaning
- **THEN** the committed summary's `## Summary` section describes or transcribes
  that figure in prose

#### Scenario: Noise figure is dropped without surfacing

- **WHEN** a localized figure is judged noise, whether by the user during the
  interview or by the LLM on the unattended path
- **THEN** it is not distilled into the summary nor promoted to `wiki/assets/`,
  and its `raw/assets/` bytes are left in place

#### Scenario: Summary structure is unchanged

- **WHEN** a summary is committed for a source with localized images
- **THEN** the page still has exactly the `## Summary` and `## Why this matters`
  sections, with figure descriptions contained within `## Summary`

### Requirement: Lazy promotion of must-see figures to wiki/assets

A localized figure SHALL be copied into `wiki/assets/` only when it must be
*seen* on the published site (prose cannot substitute). On the interactive path
this requires the user's approval during the interview. On the **unattended path
the LLM SHALL make that call itself**, promoting only figures whose meaning prose
cannot carry — a diagram, schematic, or plot — and never bulk-copying a source's
images. The `wiki/assets/` directory SHALL be created on first such promotion, not
speculatively. The promoted copy SHALL be embedded in the summary via an
Obsidian-compatible image reference; the original under `raw/assets/<twin-stem>/`
remains the immutable source of truth. An unattended promotion SHALL be recorded in
the `wiki/log.md` entry for that ingest so it is visible at review, and SHALL be
reversible: rejecting or revising the page during `curate` removes the promoted
copy from `wiki/assets/` while leaving the `raw/assets/` original in place.

#### Scenario: Figure is promoted on demand

- **WHEN** the user approves displaying a figure on the published site
- **THEN** a copy is placed under `wiki/assets/` and embedded in the summary,
  while the raw original is retained

#### Scenario: Unattended promotion is autonomous and logged

- **WHEN** the unattended path judges a localized figure to be one prose cannot
  replace
- **THEN** it promotes that figure to `wiki/assets/`, embeds it in the summary, and
  records the promotion in that ingest's `wiki/log.md` entry

#### Scenario: Unattended promotion is reversible

- **WHEN** a provisional page with an unattended figure promotion is rejected or
  has that figure removed during `curate`
- **THEN** the promoted copy is deleted from `wiki/assets/` and the
  `raw/assets/` original remains

#### Scenario: No promotion means no wiki/assets churn

- **WHEN** a source's figures are localized but none need to be displayed
- **THEN** no files are written under `wiki/assets/` and the directory is not
  created for that source

#### Scenario: Promoted figures publish via Quartz

- **WHEN** the site is built after a figure is promoted to `wiki/assets/`
- **THEN** the figure is served from the built site and no `raw/` content is
  published
