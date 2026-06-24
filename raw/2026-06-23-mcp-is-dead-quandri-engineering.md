---
source: https://www.quandri.io/engineering-blog/mcp-is-dead
fetched-at: 2026-06-23
converter: jina
---

Title: MCP is dead | Quandri Engineering

URL Source: https://www.quandri.io/engineering-blog/mcp-is-dead

Markdown Content:
💡

Reference: [MCP is dead. Long live the CLI](https://ejholmes.github.io/2026/02/28/mcp-is-dead-long-live-the-cli.html)

After reading the above article, we ran the experiments on our actual stack. This document covers the original argument, additional research, and our measurements.

‍

📌

**Update:** Since these measurements were taken, Claude Code has rolled out [Tool Search with Deferred Loading](https://code.claude.com/docs/en/mcp), which loads MCP tool schemas on-demand and reduces context usage by 85%+. The context bloat described in Problem 1 is largely addressed for users on current Claude Code versions. The performance, debugging, and architectural arguments below still apply.

## What's Wrong with MCP

MCP (Model Context Protocol) connects LLMs to external tools (GitHub, Linear, Notion, Slack, etc.).

Since its launch in late 2024, it's been called "the USB-C of the AI ecosystem." But developers actually using it day-to-day are starting to think differently.

‍

**TL;DR**: MCP eats context, has low reliability, and overlaps with existing CLI/API.

### Problem 1: It Devours the Context Window

The context window is the LLM's desk. When you connect MCP servers, **tool definitions alone** take up a significant chunk of that desk.

Restaurant analogy:

*   You sit down and 10 menus (MCP tool definitions) are spread across the table
*   There's no room left for actual food (your work)
*   Every time you order, the menus have to be pulled out again

We extracted and measured the actual tool definitions from the MCP servers connected in our environment. **With all 4 servers connected, 10.5% of the context window is consumed by tool definitions alone.**

#### Measurement: Tool Definition Sizes (Quandri Stack)

| MCP Server | Tools | Estimated Chars | Estimated Tokens |
| --- | --- | --- | --- |
| Linear | 42 | ~51,229 | ~12,807 |
| Notion | 14 | ~16,156 | ~4,039 |
| Slack | 12 | ~15,168 | ~3,792 |
| Postgres | 9 | ~1,755 | ~438 |
| Total | 77 | ~84,308 | ~21,077 |

#### Context Window Usage (all servers combined)**‍**

| Model | Context Window | Usage by Tool Definitions |
| --- | --- | --- |
| Claude (200K) | 200,000 tokens | 10.5% |
| GPT-4o (128K) | 128,000 tokens | 16.5% |

Linear alone accounts for over 12,800 tokens. That's 42 tool definitions always loaded, even if you only ever use `get_issue` and `save_issue`.

‍

#### Biggest Tools by Size

| Tool | Chars | ~Tokens |
| --- | --- | --- |
| linear/save_issue | 2,479 | ~619 |
| slack/search_public | 1,614 | ~403 |
| linear/list_issues | 1,588 | ~397 |
| notion/fetch | 1,379 | ~344 |
| slack/send_message | 1,248 | ~312 |

### Problem 2: Low Operational Reliability

| Issue | Detail |
| --- | --- |
| Init failure, repeated re-auth | Requires starting and maintaining a separate process |
| Slower AI responses | External server round-trip on every tool call |
| Mid-session tool death | MCP server process crashes |
| Opaque permissions | Unclear what permissions each tool actually has |

‍

Performance is a known issue. The author of the original article benchmarked Jira MCP against its REST API directly and found **MCP was 3x slower per call, and 9.4x slower on first call including initialization**. This isn't Jira-specific, it's architectural: every MCP server adds a process layer between the LLM and the underlying API. The same overhead applies to the Linear, Notion, and Slack servers in our stack.

### Problem 3: Overlaps with Existing CLI/API

| Aspect | CLI / API | MCP |
| --- | --- | --- |
| Human-machine parity | Same commands for humans and LLMs | Only exists inside LLM conversations |
| Composability | Pipes, jq, grep freely combinable | Locked to server return format |
| Debugging | Reproduce immediately in terminal | Only reproducible inside conversation context |
| Training data | Already learned from man pages, StackOverflow | Requires separate tool definitions |
| Install cost | Mostly already installed | Server setup, auth, process management needed |

### Token Comparison: MCP vs CLI for Linear Issue Lookup

**How many tokens does it cost to look up the same Linear issue?**MCP consumes ~65x more tokens than the CLI approach.

```
[ CLI approach: ~200 tokens ]
curl -s -H "Authorization: Bearer $LINEAR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ issue(id: \"ISSUE-ID\") { title state { name } assignee { name } } }"}' \
  https://api.linear.app/graphql

-> Prompt (curl command): ~50 tokens
-> Response: ~150 tokens

[ MCP approach: ~12,957 tokens ]
-> Tool definitions (always loaded): ~12,807 tokens (42 tools)
-> Tool call + response: ~150 tokens
```

`‍`

## What Are the Alternatives?

‍

#### Alternative 1: CLI-First Strategy

Provide CLI -> API -> docs, in that order. LLMs already learned from man pages and StackOverflow.

Using existing CLI directly:

*   No context wasted on tool definitions
*   Same interface for humans and AI, easy to debug
*   Freely composable with pipelines

‍

#### Alternative 2: Skills Pattern

If MCP is "spreading all menus on the table upfront", Skills is "**asking the librarian for only the book you need**".

‍

| Aspect | MCP | Skills |
| --- | --- | --- |
| Loading time | All tool definitions loaded on connect | Only loaded when needed |
| Context consumption | Always occupied | Only when in use |
| Scalability | Context pressure grows with each server | Not proportional to skill count |

The key is embedding CLI usage instructions inside Skills. Combined with Alternative 1's CLI-first strategy, this is most efficient. For example, a Linear skill:

‍

```
# Linear Issue Lookup Skill
- Linear API: https://api.linear.app/graphql
- Auth: Bearer Token ($LINEAR_TOKEN env var)
- Get issue: curl -s -H "Authorization: Bearer $LINEAR_TOKEN" -H "Content-Type: application/json" -d '{"query":"{ issue(id: \"ISSUE-ID\") { title state { name } assignee { name } } }"}' https://api.linear.app/graphql
- Search issues (GraphQL): adjust the query field for JQL-like filtering
- Results are JSON, parse with jq
```

`‍`

This way, the LLM only loads the above into context when the skill is invoked. No need to carry 42 tool definitions at all times. Just the CLI commands it needs.

## So Is MCP Really Dead?

Not entirely. MCP is still valid when:

*   **No CLI exists for the service** - web-only SaaS where MCP may be the only connection method
*   **Non-developer users** - MCP is more accessible for those who don't use terminals
*   **Real-time bidirectional communication** - scenarios beyond simple request-response

### What About Databases?

‍

Short answer: it depends.

DBs are just query execution at the end of the day. LLMs already know SQL and MongoDB queries well. Put DB info and CLI usage in a skill, and it works fine without MCP. Just give it the schema and it writes the queries.

```
# Postgres Skill
- Host: postgres://localhost:5432/myapp
- Tables: users (id, name, email), orders (id, user_id, status)
- CLI: psql -h localhost -d myapp -c "SELECT * FROM users WHERE ..."
```

`‍`

However, MCP has advantages for databases:

*   **Query safety** - MCP servers can enforce read-only mode and block dangerous queries at the server level. Skills + CLI can't stop the LLM from running `DROP TABLE`.
*   **Credential protection** - CLI approach may expose connection strings in the prompt. MCP servers manage credentials internally.

| Scenario | Recommendation | Why |
| --- | --- | --- |
| Local dev / personal DB | Skills + CLI | Light and fast. Easy to recover from mistakes. |
| Production DB / shared team | MCP | Safety guardrails are essential. Query validation and access control at the server level. |

But for most developer workflows, MCP is over-engineering.

These days, every SaaS landing page has "MCP supported" in the feature list. Whether the MCP server is stable or how much context it eats doesn't matter - the goal is checking the "we do MCP too" box. Same pattern as "AI-powered" and "blockchain-based" marketing from years past. When users actually connect, they get dozens of tool definitions loaded, initialization failures, and mid-session crashes.

## How We Use Skills at Quandri

At Quandri we use all three approaches side by side, picking what fits each service:

*   **Bash + CLI** for tools we already use day-to-day (`gh`, `psql`, `aws`). Zero context cost, full flexibility, debugs straight in the terminal.
*   **Skills** for repeatable multi-step workflows like commit drafting and PR reviews. Loaded only when invoked.
*   **MCP** for services without a strong CLI (Slack, Linear, Notion), and where team-wide auth or permission scoping matters (e.g., production database access).

We don't force one path. If a CLI already exists and authenticates locally, that's usually the lightest option. If a service has no CLI or we need uniform auth across the team, MCP earns its keep.

## Conclusion

‍

**Teaching well matters more than connecting everything.**

For us, replacing MCP servers with Skills that wrap existing CLIs freed up ~21K tokens of context, removed init failures from our daily workflow, and kept debugging in the terminal where it belongs.

Load only the tools you need, only when you need them, with CLI instructions baked in. MCP might evolve to solve these problems, but right now, Skills win.**‍**

**‍**

**‍

Measurement methodology**: 

Tool definition sizes were measured by extracting the JSON schema of each tool (name + description + parameters) from actually loaded MCP servers in our Claude Code environment. Token estimates use the ~4 chars/token heuristic. Full server estimates are extrapolated from sampled tool averages.

‍
