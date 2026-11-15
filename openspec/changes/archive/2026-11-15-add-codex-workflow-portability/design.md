# Design

## Context

See `proposal.md` for motivation and scope. `AGENTS.md` links to `CLAUDE.md`; the four wiki skills under `.agents/skills` link to canonical directories under `.claude/skills`. OpenSpec skills use the opposite layout. All are already discoverable in this Codex session.

The converter is an ordinary uv CLI and publishing uses a shell script and GitHub Actions. Neither invokes Claude. The portability issues sit in the README and figure-inspection instructions. A local smoke check also found that the sandbox cannot write the default uv cache; overriding `UV_CACHE_DIR` allowed offline canonicalization to succeed.

## Goals / Non-Goals

**Goals:** Give operators concrete invocation and launch guidance while keeping one copy of each instruction and preserving existing workflow semantics.

**Non-Goals:** Reorganize symlinks, rename the canonical conventions file, install Codex, add a scheduler or launcher script, change converter code, change permissions automatically, or edit historical OpenSpec records. Generated `allowed-tools` metadata is outside this change.

## Decisions

### Keep the existing shared layout

Document the link directions and canonical locations in the README. References to `CLAUDE.md` remain valid for both agents. Moving everything to `.agents` would add churn without fixing an observed discovery failure; duplicating files would introduce drift.

### Separate skill names from client invocation syntax

Use a small README table mapping each wiki skill to Claude's `/name` and Codex's `$name` forms. Include argument examples for `file` and `query`, and use agent-neutral skill names elsewhere where practical. Update the `query` skill's suggestion to invoke `/file` to refer to the `file` skill so shared guidance does not prescribe one client's syntax.

### Express figure inspection as a capability

In `file` and `ingest-inbox`, instruct the agent to inspect localized figures with its available image-viewing tool; mention Claude's `Read` and Codex's `view_image` as examples. Preserve the existing decisions about prose distillation, dropping noise, promotion, and interactive consent. Text-only file reads do not substitute for inspecting an image.

### Document runtime prerequisites without committing machine policy

Add a Codex headless section with a launch shape such as:

```bash
mise exec -- codex exec --sandbox workspace-write '$ingest-inbox'
```

State beside it that this selects workspace edits, not every permission the batch needs. The operator must configure the actual runner for network requests, git metadata writes and push authentication, writable uv/model caches, and any required local source paths. Claude's local permission allowlist and OpenSpec's `allowed-tools` field do not configure Codex. Verify flags against the installed CLI when implementing; the audit observed Codex CLI 0.169.0.

Explain that the skill avoids interview questions, while sandbox restrictions can still deny required operations. Do not describe the example as a complete unattended setup or recommend bypassing all sandbox controls. Keep policy and credentials local rather than committing a broad `.codex/config.toml`.

Use `mise exec -- uv run wiki-capture ...` in setup examples so mise supplies tools and `mise.local.toml` environment values even without interactive shell activation. Document `UV_CACHE_DIR` as an optional environment override to a runner-approved writable location; do not force a global cache change or put secrets in committed config. A scratch cache smoke check may use `/private/tmp` on this machine; general documentation should avoid assuming that macOS path exists everywhere.

## Risks / Trade-offs

- CLI flags and client syntax can change: verify current help and official documentation during implementation, and date or version any environment-specific notes.
- Workspace write permission alone can leave ingestion or push blocked: list the additional prerequisites explicitly and report validation limits without running a live batch.
- A fresh cache can trigger dependency or model downloads: use the existing environment for the offline smoke check and document separate cache requirements for full capture.
- Shared instruction edits affect both agents: review the diff for preserved consent gates, image judgment, and unattended semantics.

## Migration Plan

Update README and the three affected wiki skills in place; existing symlinks expose the edits to both agents. Validate links and instructions, then run offline toolchain checks. No content migration, live ingestion, commit, or push is needed for verification. Reverting the documentation and skill edits rolls back the change.
