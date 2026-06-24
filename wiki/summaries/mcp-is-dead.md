---
type: summary
title: MCP is dead
created: 2026-06-23
source: https://www.quandri.io/engineering-blog/mcp-is-dead
raw: raw/2026-06-23-mcp-is-dead-quandri-engineering.md
tags: [llm-agents, agentic-coding, context-window]
---

# MCP is dead

## Summary

An engineering post by [[chloe-kim|Chloe Kim]] at [[quandri|Quandri]] arguing
that the [[model-context-protocol|Model Context Protocol]] (MCP) is
over-engineered for most developer workflows, building on Eric Holmes's "MCP is
dead. Long live the CLI" and adding measurements from Quandri's own stack. (An
update notes Claude Code's Tool Search with Deferred Loading now loads MCP tool
schemas on demand, cutting context usage 85%+ and largely addressing the first
problem; the performance, debugging, and architectural arguments remain.)

Three problems with MCP: **context bloat** — tool definitions load up front and
always occupy the [[large-language-model|LLM]]'s context window (Quandri measured
77 tools across 4 servers consuming ~21K tokens — 10.5% of Claude's 200K window,
16.5% of GPT-4o's 128K — even if only one or two are used); **low reliability** —
a separate server process brings init/re-auth failures, mid-session crashes,
opaque permissions, and a per-call round trip (a referenced benchmark found MCP
~3× slower per call and ~9.4× slower on first call vs hitting the REST API
directly); and **redundancy with CLI/API**, which offer human-machine parity,
composability (pipes, jq, grep), terminal debugging, and existing training data.
Looking up one Linear issue cost ~200 tokens via curl vs ~12,957 via MCP (~65×).

Alternatives: a **CLI-first** strategy (CLI → API → docs) and the **Skills
pattern** — load instructions (including CLI usage) only when invoked, "asking
the librarian for only the book you need." Quandri uses all three: Bash+CLI for
everyday tools (`gh`, `psql`, `aws`), Skills for repeatable [[agentic-coding|agentic]]
workflows (commit drafting, PR review), and MCP only where a service has no
strong CLI or team-wide auth/permission scoping matters (e.g. production DB
access, where server-level read-only enforcement and credential protection are
genuine advantages). Conclusion: "teaching well matters more than connecting
everything."

## Why this matters

This is important to me because I have experienced running out of context with
MCPs, whereas CLIs manage context more effectively.
