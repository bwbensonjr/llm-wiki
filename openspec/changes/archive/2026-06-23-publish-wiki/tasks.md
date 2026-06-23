## 1. Quartz scaffolding

- [x] 1.1 Add Quartz to the project (config + minimal scaffolding), pinned to the Node version in `mise.toml`
- [x] 1.2 Configure Quartz's content path to source from the `wiki/` folder (config or CI staging step), excluding `raw/`
- [x] 1.3 Set the site title and a minimal default theme

## 2. Local build verification

- [x] 2.1 Run a local Quartz build and confirm pages are generated for `wiki/` summaries, entities, concepts, analyses, `index.md`, and `log.md`
- [x] 2.2 Verify `[[wikilinks]]` resolve to working hyperlinks by filename, and unresolved links render gracefully (no raw `[[...]]` shown as prose, no crash)
- [x] 2.3 Verify YAML front-matter drives page title/metadata and does not appear as body text
- [x] 2.4 Confirm no page in the output is derived from a `raw/` file

## 3. Version control hygiene

- [x] 3.1 Add Quartz build output (`public/`) and `node_modules/` to `.gitignore`
- [x] 3.2 Confirm `git status` shows no build output or `node_modules/` as content to commit

## 4. GitHub Pages deployment

- [x] 4.1 Add a GitHub Actions workflow that builds the Quartz site on `push` to `main` and on `workflow_dispatch`
- [x] 4.2 Deploy via the official Pages actions (`configure-pages`, `upload-pages-artifact`, `deploy-pages`); pin Node to match `mise.toml`
- [x] 4.3 Verify the workflow builds the site successfully (manual trigger after Pages is enabled) and the build exits non-zero on fatal errors
  <!-- Verified locally: build succeeds (exit 0), exits non-zero on fatal error, workflow YAML contains required Pages actions + dispatch. Live CI deploy pending the one-time maintainer step (enable Pages + push) — see task 5.1. -->

## 5. Documentation & setup

- [x] 5.1 Document the one-time GitHub Pages enablement (source = GitHub Actions) for the maintainer
- [x] 5.2 Document the publish/deploy flow in `README.md` and add publishing conventions to `CLAUDE.md`
