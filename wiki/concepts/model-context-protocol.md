---
type: concept
status: reviewed
title: Model Context Protocol
created: 2026-06-23
tags: [llm-agents, agentic-coding]
---

# Model Context Protocol

A protocol (launched late 2024, "the USB-C of the AI ecosystem") that connects
[[large-language-model|LLMs]] to external tools and services — GitHub, Linear,
Notion, Slack, databases, and more (MCP).

## Notes

Critiqued for over-engineering most developer workflows: each connected server
loads all its tool definitions up front, consuming context-window space even when
unused; runs as a separate process that adds latency and failure modes; and
overlaps with CLIs/APIs the model already knows. Proposed alternatives are a
CLI-first strategy and the Skills pattern (load tool instructions only when
invoked). MCP still earns its place where no strong CLI exists, for
non-developer/terminal-free users, or where server-level guardrails matter
(query validation, read-only enforcement, credential protection — e.g. shared
production databases). Claude Code's Tool Search with Deferred Loading mitigates
the context-bloat problem by loading tool schemas on demand.

## Sources

- [[mcp-is-dead|MCP is dead]]
