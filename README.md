# LLM Wiki

Use Claude Code to manage a knowledge wiki

The current state of the knolwedge wiki is available at
[`https://bwbensonjr.github.io/llm-wiki`](https://bwbensonjr.github.io/llm-wiki).

## Principles

- Based on Karpathy's llm-wiki: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Uses OpenSpec for design (commands and skills)
- A `/file` command/skill for specifying a new resource (normally by URI) and interactively tag and file as Markdown with YAML front-matter.
- A `/query` command/skill for querying and discussing and optionally saving analysis.
- A `/lint` command/skill for housekeeping and refining in specified ways 
- Viewable with Obsidian or on the web through a Quartz-generated wiki.

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

