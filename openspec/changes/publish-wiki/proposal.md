## Why

The wiki is local-first and Obsidian-friendly, but there is no way to share it
beyond cloning the repo. The curated `wiki/` layer — summaries, hubs, analyses,
index, and log — is meant to be read, yet `[[wikilinks]]` and YAML front-matter
render poorly anywhere except Obsidian. Publishing a browsable site makes the
corpus shareable with collaborators and readable from any browser, while keeping
the repo as the source of truth.

## What Changes

- Add a **publish** capability that builds the curated `wiki/` layer into a
  static HTML site, resolving Obsidian `[[wikilinks]]` and stripping/translating
  front-matter for display.
- Adopt **Quartz** (Node-based, Obsidian-native static site generator) as the
  renderer, configured to source from the `wiki/` folder.
- Publish **only the `wiki/` layer**. The immutable `raw/` twins are inputs to
  curation, not reader-facing content, and are excluded from the site.
- Add a **GitHub Pages deploy** path: a GitHub Actions workflow that builds the
  Quartz site on push to `main` and publishes it to GitHub Pages.
- Pin the Quartz/Node build inputs via the existing `mise` toolchain and extend
  `.gitignore` to exclude Quartz build output (`public/`) and `node_modules/`.
- Document the publish/deploy flow in the README and project conventions.

## Capabilities

### New Capabilities
- `wiki-publishing`: rendering the curated `wiki/` layer into a browsable static
  HTML site (wikilink resolution, front-matter handling, content scope) and
  deploying it to GitHub Pages via CI.

### Modified Capabilities
<!-- None. Publishing reads the existing wiki/ layer; it changes no
     resource-ingestion, corpus-query, or corpus-lint requirements. -->

## Impact

- **New dependency:** Quartz (Node) build pipeline; Node is already pinned in
  `mise.toml`. No change to the Python `wiki_ingest` converter.
- **New files:** Quartz configuration, a `.github/workflows/` deploy workflow,
  and `.gitignore` entries for build artifacts.
- **Repo settings:** GitHub Pages must be enabled with the GitHub Actions source
  (one-time, human-performed setup).
- **No change** to `raw/` or the ingest/query/lint commands.
- **Front-matter fix (in scope):** the analysis `sources:` convention used bare
  `[[a]], [[b]]`, which is invalid YAML and breaks the strict parser used by the
  publish pipeline. This change corrects it to a quoted-string YAML list
  (`sources: ["[[a]]", "[[b]]"]`) across `templates/analysis.md`, the `CLAUDE.md`
  spec, and the one existing analysis page. Obsidian still renders the links.
