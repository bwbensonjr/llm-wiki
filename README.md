# LLM Wiki

Use Claude Code or Codex to manage a knowledge wiki.

The current state of the knolwedge wiki is available at
[`https://bwbensonjr.github.io/llm-wiki`](https://bwbensonjr.github.io/llm-wiki).

## Principles

- Based on Karpathy's llm-wiki: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Uses OpenSpec for design (commands and skills)
- A source can be filed interactively, one sitting at a time, or queued in
  `inbox.md` and ingested unattended in a batch.
- A `file` skill for specifying a new resource (normally by URI) and interactively tagging and filing it as Markdown with YAML front-matter.
- An `ingest-inbox` skill for draining a queue of links unattended, with no interview.
- A `query` skill for querying and discussing and optionally saving analysis.
- A `lint` skill for housekeeping and refining in specified ways.
- Viewable with Obsidian or on the web through a Quartz-generated wiki.

## Sources

`wiki-capture` routes by source: web pages through Jina Reader, PDFs through
Docling, PostScript through ghostscript then Docling, other documents through
MarkItDown, and YouTube videos through their transcript.

## Ingesting via `inbox.md`

Besides the `file` skill, sources can be queued in `inbox.md` at the repo root and
ingested later in a batch. Add one checklist line per source, with an optional
note on why it matters:

```markdown
- [ ] https://example.com/some-article — good overview of closure conversion
```

Then run the `ingest-inbox` skill (see the invocation table below).
Each entry is checked off (`- [x]`) when filed, or
parked (`- [!]`) with a reason if it fails.

## Commands

Run skills from the repository root using your agent's invocation syntax:

| Skill | Claude Code | Codex |
| --- | --- | --- |
| File a source | `/file https://example.com/article` | `$file https://example.com/article` |
| Query the wiki | `/query What do the sources say about closure conversion?` | `$query What do the sources say about closure conversion?` |
| Audit the wiki | `/lint` | `$lint` |
| Drain the inbox | `/ingest-inbox` | `$ingest-inbox` |

The `file` skill also accepts a local path. See the
[Claude Code skills guide](https://code.claude.com/docs/en/skills) and
[Codex skills guide](https://developers.openai.com/codex/skills) for client details.

Instructions and skills are shared through repository symlinks:

- `AGENTS.md` links to the canonical conventions in `CLAUDE.md`.
- `.agents/skills/{file,query,lint,ingest-inbox}` link to their canonical
  directories under `.claude/skills/`.
- `.claude/skills/openspec-*` link to the canonical OpenSpec skill directories
  under `.agents/skills/`.

Edit the canonical files to keep both agents on the same instructions.

- **`file <uri-or-path>`** — ingest a source. Converts a URL or local file into
  an immutable `raw/` twin, then runs a propose→coach→commit interview to author
  a dual-voice `summary` page and update the entity/concept hubs, index, and log.
- **`ingest-inbox`** — drain the queue in `inbox.md` unattended. Runs the same
  capture, then authors the wiki layer with **no interview**: it classifies,
  titles, tags, links and creates hubs, judges figures, and drafts
  `## Why this matters` — seeded by the note you left on the inbox line. It
  skips links already ingested,
  refuses to author from a paywall or error-page capture, isolates each entry's
  failures, commits per source, and pushes once at the end. Never asks an
  interview question. Headless runs require the runtime setup described below.
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

## Running Codex headlessly

From the repository root, invoke the inbox skill with Codex's non-interactive CLI:

```bash
mise exec -- codex exec --sandbox workspace-write '$ingest-inbox'
```

The single quotes preserve the literal `$ingest-inbox` prompt. The sandbox flag
selects workspace edits; the runner still needs access for the complete batch:

- Writes to the repository content and git metadata for per-source commits.
- Network access to source and converter services and the git remote.
- Codex authentication, `JINA_API_KEY` for web capture, and git credentials
  usable without an interactive login for pull and push.
- Writable uv and converter model caches, including space for initial downloads.
- Read access to any local source paths queued outside the repository.

Configure these permissions for the actual runner before scheduling a batch.
Also configure a non-interactive approval policy for that runner so operations
either run with the required permissions or fail with a report instead of waiting
for a human response. Keep the workspace sandbox in place.
The skill asks no interview questions, but sandbox or approval restrictions can
still deny required operations. `.claude/settings.local.json` configures Claude
Code; it grants no Codex permissions. The generated OpenSpec skills'
`allowed-tools` metadata also grants no Codex permissions. Keep credentials and
machine-specific policy local.

See [Codex non-interactive mode](https://developers.openai.com/codex/noninteractive)
for runtime configuration. The flags above were checked with Codex CLI 0.169.0;
check `codex exec --help` when configuring a different version.

Use `mise exec --` when invoking tools without interactive shell activation. It
supplies the project toolchain and environment, including local values from the
gitignored `mise.local.toml`. For example, this offline check canonicalizes a
YouTube URL and writes no raw twin or wiki page:

```bash
mise exec -- uv run --no-sync wiki-capture --canonical 'https://youtu.be/dQw4w9WgXcQ?si=example'
```

This check assumes the uv project environment is already installed. For first
setup, run `mise exec -- uv sync` with access to dependency downloads and a
writable cache.

If the default uv cache is outside the sandbox's writable paths, set
`UV_CACHE_DIR` to a runner-approved writable directory. For example, if the
runner allows writes to `/tmp`, the offline check can use:

```bash
UV_CACHE_DIR=/tmp/llm-wiki-uv-cache mise exec -- uv run --no-sync wiki-capture --canonical 'https://youtu.be/dQw4w9WgXcQ?si=example'
```

The same override can prefix the headless Codex command. It controls uv's cache;
full capture also needs writable caches for the converters and their models.
Store `JINA_API_KEY` in the gitignored `mise.local.toml`, as described in
`CLAUDE.md`; keep committed `mise.toml` secret-free.

