# wiki-publishing Specification

## Purpose

Publish the curated `wiki/` layer as a browsable static HTML site so the
knowledge wiki can be read outside Obsidian. The site is built from `wiki/`
content only (never the immutable `raw/` twins) using Quartz, resolves the
wiki's Obsidian-style `[[wikilinks]]`, and is deployed to GitHub Pages on every
push to `main`. Generated build output and the Node dependency tree stay out of
version control.

## Requirements

### Requirement: Static site build from the wiki layer

The system SHALL build a browsable static HTML site from the curated `wiki/`
layer using Quartz. The build SHALL source content exclusively from `wiki/` and
SHALL produce self-contained static output (HTML, CSS, JS) suitable for hosting.

#### Scenario: Build produces a site from wiki content

- **WHEN** the publish build runs against a repo containing `wiki/` pages
- **THEN** a static site is generated whose pages correspond to the Markdown
  files under `wiki/` (summaries, entities, concepts, analyses, index, log)

#### Scenario: Build fails loudly on error

- **WHEN** the build encounters a fatal error (missing config, renderer failure)
- **THEN** the build exits non-zero and writes no partial published output as
  the final artifact

### Requirement: Content scope excludes the raw layer

The published site SHALL include only the `wiki/` layer. The immutable `raw/`
twins SHALL NOT appear as pages in the published site.

#### Scenario: Raw twins are absent from output

- **WHEN** the site is built from a repo containing both `raw/` and `wiki/`
- **THEN** no page in the published output is derived from a `raw/` file

### Requirement: Obsidian wikilink resolution

The renderer SHALL resolve Obsidian-style `[[wikilinks]]` to working hyperlinks
in the published HTML, resolving by page filename (slug) independent of folder,
consistent with the wiki's linking convention.

#### Scenario: Wikilink resolves to its target page

- **WHEN** a published page contains `[[some-slug]]` and a page with that slug
  exists in `wiki/`
- **THEN** the rendered link points to that target page's published URL

#### Scenario: Unresolved wikilink is handled gracefully

- **WHEN** a published page contains a `[[wikilink]]` with no matching target
- **THEN** the build does not crash and the link is rendered as inert text or a
  clearly broken link, not raw `[[...]]` syntax silently treated as prose

### Requirement: Front-matter handling

The renderer SHALL consume YAML front-matter (e.g. `title`, `tags`) for display
metadata and SHALL NOT render raw front-matter blocks as page body text.

#### Scenario: Front-matter drives title, not body

- **WHEN** a `wiki/` page with YAML front-matter is published
- **THEN** the page uses its `title` for the page heading/metadata and the raw
  `---` front-matter block does not appear in the rendered body

### Requirement: GitHub Pages deployment on push to main

The system SHALL provide a GitHub Actions workflow that builds the site and
deploys it to GitHub Pages when changes are pushed to the `main` branch. The
workflow SHALL also be manually triggerable.

#### Scenario: Push to main deploys the site

- **WHEN** a commit is pushed to `main`
- **THEN** the workflow builds the Quartz site and publishes it to GitHub Pages

#### Scenario: Manual trigger

- **WHEN** a maintainer triggers the workflow manually (workflow_dispatch)
- **THEN** the site is built and deployed using the current `main` content

### Requirement: Build artifacts excluded from version control

Generated build output and the Node dependency tree SHALL be excluded from git
via `.gitignore` so that machine-local and regenerated state is never committed.

#### Scenario: Build output is gitignored

- **WHEN** the site is built locally, producing Quartz output and
  `node_modules/`
- **THEN** `git status` shows neither the build output directory nor
  `node_modules/` as untracked content to commit
