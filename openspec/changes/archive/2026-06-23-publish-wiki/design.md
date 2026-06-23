## Context

llm-wiki is a local-first git repo of Markdown with a two-layer store: immutable
`raw/` twins and an evolving curated `wiki/` layer (summaries, entity/concept
hubs, analyses, `index.md`, `log.md`). Pages use YAML front-matter and
Obsidian-style `[[wikilinks]]` that resolve by filename regardless of folder.
Today the only way to read the corpus is to clone the repo or open it in
Obsidian; there is no shareable, browser-readable form.

The toolchain is managed by `mise`, which already pins `node`, `python`, `uv`,
and the `openspec` CLI. The Python `wiki_ingest` project owns conversion/ingest;
publishing is a separate, read-only concern over the `wiki/` layer.

## Goals / Non-Goals

**Goals:**
- Render the `wiki/` layer into a browsable static HTML site with faithful
  `[[wikilink]]` resolution and clean front-matter handling.
- Deploy that site to GitHub Pages automatically on push to `main`.
- Keep the git repo the single source of truth; published output is derived and
  never committed.
- Reuse the existing `mise`/Node toolchain; add no Python dependencies.

**Non-Goals:**
- Publishing the `raw/` layer or any machine-local state.
- Changing ingest, query, or lint behavior or any existing `wiki/` content.
- A custom renderer or authentication/access control on the published site.
- A local `wiki-publish` CLI command (the human builds via Quartz/CI; a local
  preview is available through Quartz's own dev server but is not a new command).

## Decisions

**Decision: Use Quartz as the renderer.**
Quartz is purpose-built for publishing Obsidian vaults: it resolves `[[wikilinks]]`
by filename, consumes YAML front-matter, supports backlinks/graph views, and
emits a self-contained static site. Rationale: highest fidelity to this repo's
Obsidian conventions with the least glue code.
- *Alternatives considered:* **MkDocs + a wikilink plugin** — mature and
  themeable but wikilink support is bolt-on and folder-sensitive, needing more
  config to match Obsidian semantics. **Custom Python renderer in `wiki_ingest`**
  — full control but reimplements wikilink resolution, backlinks, and theming
  that Quartz already provides; rejected as avoidable maintenance.

**Decision: Source Quartz from the `wiki/` folder only.**
Quartz reads from a content directory; point it at `wiki/` (not repo root) so the
`raw/` layer is structurally excluded rather than filtered. Rationale: scope is
enforced by configuration, satisfying the "raw excluded" requirement by default.
- *Implementation note:* Quartz conventionally expects content under `content/`.
  Configure Quartz's content path to `wiki/` directly (via config or a build-time
  symlink/copy step in CI) so no content is duplicated in git.

**Decision: Deploy via GitHub Actions to GitHub Pages.**
A workflow on `push` to `main` (plus `workflow_dispatch`) builds the site and
publishes with the official Pages actions (`actions/configure-pages`,
`actions/upload-pages-artifact`, `actions/deploy-pages`). Rationale: matches the
existing "file ingests commit to main" flow — publishing follows main with no
extra branch dance. Pin Node in the workflow to match `mise.toml`.
- *Alternatives considered:* deploy to a `gh-pages` branch via a third-party
  action — older pattern, commits build output into git history, which violates
  the repo's "never commit generated state" rule.

**Decision: Gitignore build output and `node_modules/`.**
Add Quartz's output dir (`public/`) and `node_modules/` to `.gitignore`.
Rationale: consistent with the repo's existing rule that regenerated or
machine-local state stays untracked.

## Risks / Trade-offs

- **Quartz expects a vault-shaped `content/` dir, not arbitrary roots** →
  Configure the content path to `wiki/` or stage a copy/symlink in the CI build
  step; verify locally before wiring CI.
- **`index.md` / `log.md` semantics** → these are bookkeeping pages; Quartz will
  publish them as ordinary pages. Acceptable (they aid navigation); revisit if
  `log.md` grows unwieldy. Not excluded for now.
- **New Node ecosystem surface (Quartz deps)** → pin Node version in CI to match
  `mise.toml`; `node_modules/` stays gitignored so churn never hits the repo.
- **GitHub Pages requires one-time manual enablement** (Pages source = GitHub
  Actions) → documented as a human setup step; the workflow cannot self-enable
  Pages.
- **Broken/unresolved wikilinks** → Quartz renders them as broken links rather
  than crashing; lint (`corpus-lint`) remains the place to catch these at the
  source.

## Migration Plan

1. Add Quartz (config + minimal scaffolding) pointed at `wiki/`; build locally
   and confirm wikilinks, front-matter, and raw-exclusion behave.
2. Add `.gitignore` entries for `public/` and `node_modules/`.
3. Add the GitHub Actions deploy workflow (`push: main` + `workflow_dispatch`).
4. Human enables GitHub Pages with the GitHub Actions source (one-time).
5. Document the publish/deploy flow in README and CLAUDE.md conventions.
- *Rollback:* the change is additive and read-only over `wiki/`; reverting the
  config, workflow, and `.gitignore` entries fully removes publishing with no
  effect on corpus content.

## Open Questions

- Should `log.md` be excluded from the public site once it grows long? (Default:
  publish it; revisit later.)
- Theme/branding for the Quartz site — accept defaults initially, or set a title
  and minimal theme as part of this change? (Default: minimal — set site title
  only.)
