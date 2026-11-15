# Tasks

## 1. Document agent invocation and shared instructions

- [x] 1.1 Update README to name Claude Code and Codex, explain the existing conventions and skill symlink directions, and provide an invocation table for `file`, `query`, `lint`, and `ingest-inbox`, including source and question arguments. Verify each documented path resolves and compare syntax with current client documentation.
- [x] 1.2 Make remaining README references to skill invocation consistent with the table and replace the shared `query` skill's `/file` suggestion with an agent-neutral reference. Verify a targeted search for slash commands leaves only explicitly Claude examples in these edited files.

## 2. Make figure inspection instructions portable

- [x] 2.1 Update `file` and `ingest-inbox` to require visual inspection with the available image tool, using `Read` and `view_image` only as agent-specific examples. Review the diff to verify that distillation, dropping, promotion, and interactive consent rules remain intact and that text-only reads are not presented as image inspection.
- [x] 2.2 Verify the edits are visible through both `.claude/skills` and `.agents/skills` and that all four wiki skills retain valid name and description metadata. Check link targets and inspect the shared files without copying or reorganizing them.

## 3. Document and verify Codex runtime setup

- [x] 3.1 Add README guidance for `codex exec` with a single-quoted `$ingest-inbox` prompt and explicit workspace-write selection. Verify flags with the installed `codex exec --help`; document that the example still requires runner-specific network access, git metadata writes, credentials, and writable dependency/model caches, and that Claude settings and generated `allowed-tools` metadata grant none of these Codex permissions.
- [x] 3.2 Document `mise exec --` for non-interactive tool and environment loading and an optional `UV_CACHE_DIR` override to a runner-approved writable path. Verify offline canonicalization with the existing environment using `mise exec -- uv run --no-sync wiki-capture --canonical <youtube-share-url>` and a scratch cache when needed; confirm canonical JSON output and no raw or wiki writes. Do not print secrets or run live ingestion to validate setup.
- [x] 3.3 Review the complete implementation diff and run `mise exec -- openspec validate add-codex-workflow-portability --strict`. Verify changes are limited to the README and three shared wiki skills plus planning artifacts; report that full headless capture, commits, and push were not exercised. Preserve existing symlinks, machine configuration, generated OpenSpec skills, and historical records.
