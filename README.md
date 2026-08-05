# LLM Wiki

Use Claude Code to manage a knowledge wiki

The current state of the knolwedge wiki is available at
[`https://bwbensonjr.github.io/llm-wiki`](https://bwbensonjr.github.io/llm-wiki).

## Principles

- Based on Karpathy's llm-wiki: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Uses OpenSpec for design (commands and skills)
- **Capture cadence and review cadence are decoupled.** A source can be filed
  interactively, one sitting at a time, or captured unattended in a batch and
  reviewed later. Human judgment is moved, not removed: machine-authored pages
  land as `status: provisional` and are endorsed, corrected, or rejected
  afterward.
- A `/file` command/skill for specifying a new resource (normally by URI) and interactively tag and file as Markdown with YAML front-matter.
- An `/ingest-inbox` command/skill for draining a queue of links unattended, with no interview.
- A `/curate` command/skill for reviewing what was ingested unattended.
- A `/query` command/skill for querying and discussing and optionally saving analysis.
- A `/lint` command/skill for housekeeping and refining in specified ways 
- Viewable with Obsidian or on the web through a Quartz-generated wiki.

## Commands

- **`file <uri-or-path>`** — ingest a source. Converts a URL or local file into
  an immutable `raw/` twin, then runs a propose→coach→commit interview to author
  a dual-voice `summary` page and update the entity/concept hubs, index, and log.
- **`ingest-inbox`** — drain the queue in `inbox.md` unattended. Runs the same
  capture, then authors the wiki layer with **no interview**: it classifies,
  titles, tags, links and creates hubs, judges figures, and drafts
  `## Why this matters` — seeded by the note you left on the inbox line. Every
  page it writes is `status: provisional`. It skips links already ingested,
  refuses to author from a paywall or error-page capture, isolates each entry's
  failures, commits per source, and pushes once at the end. Never asks a
  question, so it is safe to run headlessly.
- **`curate`** — review the provisional queue: every page carrying
  `status: provisional`, derived from front-matter rather than a maintained list.
  Presents each page with its corpus-relational context — what it links, what it
  duplicates, what it contradicts, which tags are new — and clusters
  near-duplicate hubs. Verbs: endorse, edit-then-endorse, retag, reclassify,
  merge hub, and reject (which deletes the page and unlinks it; the `raw/` twin
  survives). Reports read-only by default; writes only on your commit.
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

