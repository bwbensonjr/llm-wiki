# Proposal

## Why

Codex now discovers the project's shared instructions and skills through repository symlinks, but the README still assumes Claude Code and two shared skills name Claude's image-reading tool. Codex also needs explicit guidance for headless permissions, mise environment loading, and sandbox-writable uv caches to run the existing workflows reliably.

## What Changes

- Document Claude Code and Codex as supported agents, with invocation examples for all four wiki skills: Claude slash commands and Codex `$skill` syntax.
- Explain the existing `AGENTS.md` and skill symlink layout and its shared source of truth.
- Replace literal `Read` tool calls in the `file` and `ingest-inbox` figure instructions with capability-based image inspection guidance, including Codex's `view_image` as an example.
- Make the `query` skill's suggestion to invoke `/file` refer to the `file` skill without prescribing client syntax.
- Document a Codex headless launch example and the required runtime access: repository writes, git metadata writes, network access, credentials, and writable dependency caches. Distinguish these runtime prerequisites from the skill's instruction to ask no interview questions.
- Document explicit `mise exec --` commands and an optional `UV_CACHE_DIR` override when the default uv cache is outside the sandbox.
- Preserve existing links, converter behavior, publication behavior, interactive review gates, and unattended failure handling.

## Capabilities

### New Capabilities

None. This change documents operation of existing capabilities with a second agent.

### Modified Capabilities

None. The `resource-ingestion` and `unattended-ingestion` specifications already describe agent-independent behavior. Image inspection remains required; only the tool-specific wording changes. This change sets `skip_specs: true` because it changes documentation and instruction portability without changing those requirements.

## Impact

- `README.md`: supported agents, skill invocation, shared links, and headless setup guidance.
- `.claude/skills/file/SKILL.md` and `.claude/skills/ingest-inbox/SKILL.md`: portable figure inspection wording, visible to Codex through the existing `.agents/skills` symlinks.
- `.claude/skills/query/SKILL.md`: agent-neutral reference to the `file` skill.
- No Python, dependency, publishing workflow, machine-local permission configuration, or wiki content changes.
- Generated OpenSpec metadata and historical Claude references remain as installed or recorded; they are not Codex permission grants.
