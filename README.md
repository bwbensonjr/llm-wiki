# LLM Wiki

Use Claude Code to manage a knowledge wiki

## Design References

- Based on Karpathy's llm-wiki: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Using OpenSpec for design (commands and skills)

## Commands

- **`file <uri-or-path>`** — ingest a source. Converts a URL or local file into
  an immutable `raw/` twin, then runs a propose→coach→commit interview to author
  a dual-voice `summary` page and update the entity/concept hubs, index, and log.
- **`query <question>`** — interrogate the corpus. Surveys the index, reads the
  relevant summary/entity/concept pages, and synthesizes a cited, corpus-grounded
  answer. Optionally files the answer back as an `analysis` page via the same
  propose→coach→commit interview, updating the index and log. Answers in
  conversation by default; writes nothing to the wiki unless you commit.
- **`lint`** — audit the whole corpus for consistency defects: invalid or
  incomplete front-matter, `type`/folder mismatches, broken wikilinks, orphan
  pages, index/log drift, missing body sections, and near-duplicate tags. Reports
  read-only by default; optionally repairs via the same propose→coach→commit
  interview, separating safe mechanical fixes from judgment calls (like tag
  merges) and previewing changes before writing. Never touches `raw/`.

## Publishing

The curated `wiki/` layer can be published as a browsable static site with
[Quartz](https://quartz.jzhao.xyz) and hosted on GitHub Pages. Only `wiki/` is
published; the immutable `raw/` twins are excluded.

**Build locally:**

```sh
bash scripts/build-site.sh   # clones pinned Quartz into .quartz/, builds wiki/ -> public/
```

The script clones a pinned Quartz into `.quartz/`, overlays `quartz.config.ts`,
and renders `wiki/` (resolving `[[wikilinks]]` by filename) into `public/`. All
three of `public/`, `.quartz/`, and `node_modules/` are gitignored.

**Deploy:** `.github/workflows/publish.yml` builds and deploys to GitHub Pages on
every push to `main` (and on manual `workflow_dispatch`).

**One-time setup (maintainer):** in the GitHub repo, go to
**Settings → Pages → Build and deployment** and set **Source** to
**GitHub Actions**. The workflow cannot enable Pages itself. Once enabled, the
site publishes at `https://bwbensonjr.github.io/llm-wiki/` (the `baseUrl` set in
`quartz.config.ts`).

## Ideas

- Follow the main principles of Karpathy's design 
- Create a command for specifying a new resource (normally by URI) and interactively discussing and filing 
- Produce a local Markdown version of the resource with YAML front-matter 
- Create in a way allowing for Obisdian viewing 

